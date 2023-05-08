from dicee.executer import Execute
import pytest
from dicee.config import Args

class TestRegressionConEx:
    @pytest.mark.filterwarnings('ignore::UserWarning')
    def test_k_vs_all(self):
        args = Args()
        args.model = 'ConEx'
        args.scoring_technique = 'KvsAll'
        args.optim = 'Adam'
        args.path_dataset_folder = 'KGs/UMLS'
        args.num_epochs = 20
        args.batch_size = 1024
        args.lr = 0.01
        args.embedding_dim = 32
        args.input_dropout_rate = 0.0
        args.hidden_dropout_rate = 0.0
        args.feature_map_dropout_rate = 0.0
        args.eval_model = 'train_val_test'
        args.read_only_few = None
        args.sample_triples_ratio = None
        args.num_folds_for_cv = None
        args.normalization = 'LayerNorm'
        args.trainer = 'torchCPUTrainer'
        args.init_param = 'xavier_normal'
        result = Execute(args).start()
        assert 0.46 >= result['Train']['H@1'] >= 0.32
        assert 0.46 >= result['Val']['H@1'] >= 0.32
        assert 0.46 >= result['Test']['H@1'] >= 0.30

    @pytest.mark.filterwarnings('ignore::UserWarning')
    def test_1_vs_all(self):
        args = Args()
        args.model = 'ConEx'
        args.path_dataset_folder = 'KGs/UMLS'
        args.num_epochs = 10
        args.batch_size = 1024
        args.lr = 0.1
        args.embedding_dim = 32
        args.input_dropout_rate = 0.0
        args.hidden_dropout_rate = 0.0
        args.feature_map_dropout_rate = 0.0
        args.eval_model = 'train_val_test'
        args.sample_triples_ratio = None
        args.read_only_few = None
        args.num_folds_for_cv = None
        args.normalization = 'LayerNorm'
        args.scoring_technique = '1vsAll'
        args.trainer = 'torchCPUTrainer'
        args.init_param = 'xavier_normal'
        result = Execute(args).start()
        assert 0.75 >= result['Train']['H@1'] > 0.02
        assert 0.75 >= result['Val']['H@1'] >= 0.02
        assert 0.75 >= result['Test']['H@1'] >= 0.02

    @pytest.mark.filterwarnings('ignore::UserWarning')
    def test_negative_sampling(self):
        args = Args()
        args.model = 'ConEx'
        args.path_dataset_folder = 'KGs/UMLS'
        args.num_epochs = 50
        args.batch_size = 1024
        args.lr = 0.01
        args.embedding_dim = 32
        args.input_dropout_rate = 0.0
        args.hidden_dropout_rate = 0.0
        args.feature_map_dropout_rate = 0.0
        args.scoring_technique = 'NegSample'
        args.eval_model = 'train_val_test'
        args.sample_triples_ratio = None
        args.num_folds_for_cv = None
        args.read_only_few = None
        args.neg_ratio = 1
        args.normalization = 'LayerNorm'
        args.trainer = 'torchCPUTrainer'
        args.init_param = 'xavier_normal'
        result = Execute(args).start()
        assert 0.77 >= result['Train']['H@1'] >= .20
        assert 0.70 >= result['Val']['H@1'] >= .20
        assert 0.70 >= result['Test']['H@1'] >= .20

    # TODO: Write Test and compare ConEx with AConEx
