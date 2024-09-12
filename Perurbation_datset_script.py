import pickle
import os.path as osp
import numpy as np
import click
import random
import torch

def index_dataset(dataset_name, force=False):
    print('Indexing dataset {0}'.format(dataset_name))
    base_path = f'{dataset_name}/'
    files = ['train.txt', 'valid.txt', 'test.txt']
    indexified_files = ['train_indexified.txt', 'valid_indexified.txt', 'test_indexified.txt']
    return_flag = True
    for i in range(len(indexified_files)):
        if not osp.exists(osp.join(base_path, indexified_files[i])):
            return_flag = False
            break
    if return_flag and not force:
        print("Index file exists")
        return  

    ent2id, rel2id, id2rel, id2ent = {}, {}, {}, {}

    entid, relid = 0, 0

    with open(osp.join(base_path, files[0])) as f:
        lines = f.readlines()
        file_len = len(lines)

    for p, indexified_p in zip(files, indexified_files):
        fw = open(osp.join(base_path, indexified_p), "w")
        with open(osp.join(base_path, p), 'r') as f:
            for i, line in enumerate(f):
                print(f'[{i}/{file_len}]', end='\r')
                e1, rel, e2 = line.split('\t')
                e1 = e1.strip()
                e2 = e2.strip()
                rel = rel.strip()

                if p == "train.txt":
                    if e1 not in ent2id.keys():
                        ent2id[e1] = entid
                        id2ent[entid] = e1
                        entid += 1

                    if e2 not in ent2id.keys():
                        ent2id[e2] = entid
                        id2ent[entid] = e2
                        entid += 1

                    if rel not in rel2id.keys():
                        rel2id[rel] = relid
                        id2rel[relid] = rel
                        relid += 1

                if e1 in ent2id.keys() and e2 in ent2id.keys():
                    fw.write("\t".join([str(ent2id[e1]), str(rel2id[rel]), str(ent2id[e2])]) + "\n")
        fw.close()

    with open(osp.join(base_path, "stats.txt"), "w") as fw:
        fw.write("numentity: " + str(len(ent2id)) + "\n")
        fw.write("numrelations: " + str(len(rel2id)))
    with open(osp.join(base_path, 'ent2id.pkl'), 'wb') as handle:
        pickle.dump(ent2id, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(osp.join(base_path, 'rel2id.pkl'), 'wb') as handle:
        pickle.dump(rel2id, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(osp.join(base_path, 'id2ent.pkl'), 'wb') as handle:
        pickle.dump(id2ent, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(osp.join(base_path, 'id2rel.pkl'), 'wb') as handle:
        pickle.dump(id2rel, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print(f'Num entity: {len(ent2id)}, num relation: {len(rel2id)}')
    print("Indexing finished!!")

def perturb_data(x, ratio, num_entities, num_relations, id2ent, id2rel):
    n = x.size(0)
    num_of_perturbed_data = int(n * ratio)
    if num_of_perturbed_data == 0:
        return x, []

    device = x.device
    random_indices = torch.randperm(n, device=device)[:num_of_perturbed_data]

    perturbed_triples = []
    for idx in random_indices:
        original_triple = x[idx].tolist()
        e1, rel, e2 = original_triple

        # Get the relation name
        rel_name = id2rel[rel]

        # Skip perturbation if the relation is 'isa'
        if rel_name == 'isa':
            continue

        # Randomly choose whether to perturb the entity or relation
        if torch.rand(1) > 0.5:
            # Perturb the entity (subject or object)
            perturbation = torch.randint(low=0, high=num_entities, size=(1,), device=device)
            x[idx, 0] = perturbation
        else:
            # Perturb the relation but ensure it's not 'isa'
            while True:
                perturbation = torch.randint(low=0, high=num_relations, size=(1,), device=device)
                if id2rel[perturbation.item()] != 'isa':
                    x[idx, 1] = perturbation
                    break

        perturbed_triples.append((original_triple, x[idx].tolist()))

    return x, perturbed_triples

def load_triples(file_path, ent2id, rel2id):
    triples = []
    with open(file_path, 'r') as f:
        for line in f:
            e1, rel, e2 = line.strip().split('\t')
            triples.append([ent2id[e1], rel2id[rel], ent2id[e2]])
    return torch.tensor(triples, dtype=torch.long)

def save_triples(file_path, triples, id2ent, id2rel):
    with open(file_path, 'w') as f:
        for triple in triples:
            e1, rel, e2 = triple.tolist()
            f.write(f"{id2ent[e1]}\t{id2rel[rel]}\t{id2ent[e2]}\n")

@click.command()
@click.option('--dataset_path', default="UMLS", help="Path to the knowledge graph dataset")
@click.option('--file_type', default='train', type=click.Choice(['train', 'valid', 'test']), help="Type of file to perturb")
@click.option('--ratio', default=0.01, type=float, help="Ratio of data to perturb")
@click.option('--seed', default=42, type=int, help="Random seed for reproducibility")
def main(dataset_path, file_type, ratio, seed):
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)

    base_path = dataset_path
    index_dataset(base_path)

    ent2id = pickle.load(open(osp.join(base_path, "ent2id.pkl"), 'rb'))
    rel2id = pickle.load(open(osp.join(base_path, "rel2id.pkl"), 'rb'))
    id2ent = pickle.load(open(osp.join(base_path, "id2ent.pkl"), 'rb'))
    id2rel = pickle.load(open(osp.join(base_path, "id2rel.pkl"), 'rb'))

    file_path = osp.join(base_path, f"{file_type}.txt")
    triples = load_triples(file_path, ent2id, rel2id)

    num_entities = len(ent2id)
    num_relations = len(rel2id)

    perturbed_triples, perturbed_details = perturb_data(triples, ratio, num_entities, num_relations, id2ent, id2rel)

    output_indexified_file = osp.join(base_path, f"{file_type}_perturbed_indexified.txt")
    torch.save(perturbed_triples, output_indexified_file)

    output_txt_file = osp.join(base_path, f"{file_type}_perturbed.txt")
    save_triples(output_txt_file, perturbed_triples, id2ent, id2rel)

     # File to save the perturbation details
    perturbation_log_file = osp.join(base_path, "perturbation_log.txt")

    # Open the file and write the perturbation details
    with open(perturbation_log_file, "w") as log_file:
        for original, perturbed in perturbed_details:
            original_triplet = f"({id2ent[original[0]]}, {id2rel[original[1]]}, {id2ent[original[2]]})"
            perturbed_triplet = f"({id2ent[perturbed[0]]}, {id2rel[perturbed[1]]}, {id2ent[perturbed[2]]})"
            log_file.write(f"Original: {original_triplet} -> Perturbed: {perturbed_triplet}\n")

    print(f"Perturbed data saved to {output_indexified_file} and {output_txt_file}")
    print(f"Perturbation details saved to {perturbation_log_file}")


if __name__ == '__main__':
    main()
