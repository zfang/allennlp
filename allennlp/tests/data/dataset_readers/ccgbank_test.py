from allennlp.data.dataset_readers import CcgBankDatasetReader
from allennlp.common.util import ensure_list
from allennlp.common.testing import AllenNlpTestCase
from allennlp.data.vocabulary import Vocabulary


class TestCcgBankReader(AllenNlpTestCase):

    def test_read_from_file(self):

        reader = CcgBankDatasetReader()
        instances = ensure_list(reader.read(self.FIXTURES_ROOT / 'data' / 'ccgbank.txt'))

        assert len(instances) == 2

        instance = instances[0]
        fields = instance.fields
        tokens = [token.text for token in fields['tokens'].tokens]
        assert tokens == ['Pierre', 'Vinken', ',', '61', 'years', 'old', ',', 'will', 'join', 'the', 'board',
                          'as', 'a', 'nonexecutive', 'director', 'Nov.', '29', '.']

        ccg_categories = fields['ccg_categories'].labels
        assert ccg_categories == ['N/N', 'N', ',', 'N/N', 'N', '(S[adj]\\NP)\\NP', ',', '(S[dcl]\\NP)/(S[b]\\NP)',
                                  '(S[b]\\NP)/NP', 'NP[nb]/N', 'N', '((S\\NP)\\(S\\NP))/NP', 'NP[nb]/N', 'N/N',
                                  'N', '((S\\NP)\\(S\\NP))/N[num]', 'N[num]', '.']

        original_pos_tags = fields['original_pos_tags'].labels
        assert original_pos_tags == ['NNP', 'NNP', ',', 'CD', 'NNS', 'JJ', ',', 'MD', 'VB', 'DT', 'NN',
                                     'IN', 'DT', 'JJ', 'NN', 'NNP', 'CD', '.']

        modified_pos_tags = fields['modified_pos_tags'].labels
        assert modified_pos_tags == ['NNP', 'NNP', ',', 'CD', 'NNS', 'JJ', ',', 'MD', 'VB', 'DT', 'NN',
                                     'IN', 'DT', 'JJ', 'NN', 'NNP', 'CD', '.']

        predicate_arg_categories = fields['predicate_arg_categories'].labels
        assert predicate_arg_categories == ['N_73/N_73', 'N', ',', 'N_93/N_93', 'N', '(S[adj]\\NP_83)\\NP_84',
                                            ',', '(S[dcl]\\NP_10)/(S[b]_11\\NP_10:B)_11', '(S[b]\\NP)/NP',
                                            'NP[nb]_29/N_29', 'N', '((S_1\\NP_2)_1\\(S_1\\NP_2)_1)/NP',
                                            'NP[nb]_48/N_48', 'N_43/N_43', 'N',
                                            '((S_61\\NP_56)_61\\(S_61\\NP_56)_61)/N[num]_62', 'N[num]', '.']

    def test_vocab_from_instances_namespaces(self):
        reader = CcgBankDatasetReader()
        instances = ensure_list(reader.read(self.FIXTURES_ROOT / 'data' / 'ccgbank.txt'))
        # check that we didn't clobber the labels namespace
        vocab = Vocabulary.from_instances(instances)
        self.assertSetEqual(
                set(vocab._token_to_index.keys()), # pylint: disable=protected-access
                {'tokens', 'modified_pos_tags_labels', 'original_pos_tags_labels',
                 'predicate_arg_categories_labels', 'ccg_categories_labels'}
        )
