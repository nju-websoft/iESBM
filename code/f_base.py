'''
abstract class for featutres
@file: f_base.py
@author: qxliu
@time: 2020/5/19 10:37
'''
from iesbm_utils import *
class FType(Enum):
	F_Triple = 0 # triple-level feature, e.g. LFoP, GFoP, GFoV, IoPV
	F_Set = 1 # summary-level feature, e.g. DoP, DoV

class Feature():
	'''
	base implementation to get feature for summary:
	for triple-level features: read t-level scores from file (or customize implement for new features)
	for summary-level features: by subclass F_DoP, F_DoV from f_imp (or customize implement for new features)
	'''
	def __init__(self, ds_name, fname, ftype, fpath=None):
		self.ds_name = ds_name
		self.fname = fname
		self.ftype = ftype
		self.fpath = fpath

		assert type(self.ftype)==FType

		if ftype==FType.F_Triple:
			# self.fpath = os.path.join(ROOT_DIR, 'in', 'in_ds_feature', '{}_{}.txt'.format(self.fname,ds_name)) if fpath is None else fpath
			self.fpath = os.path.join(IN_DIR, 'in_ds_feature', '{}_{}.txt'.format(self.fname,ds_name)) if fpath is None else fpath
			if not os.path.exists(self.fpath):
				raise Exception('Feature File not found! fname={}, path={}'.format(self.fname, self.fpath))
			self.tid_tscore_dict = self._read_tscore(self.fpath) # load tscore
		else:
			self.fitem = None

	def get_score(self, eid, summtids):
		'''
		get score for the summary
		i.e. for triple-level features, score(summary) = sum(TScore_t)/|summary|; -- read TScore_t from file
		for summary-level features, score(summary) = SScore(summary); -- customize implementation of SScore()
		:param ds_name:
		:param summary: for tscore, summtids; for sscore, eid or summtids
		:param feature_path:
		:return:
		'''
		if self.ftype==FType.F_Triple:
			return self._get_score_by_tscore(summtids)
		elif self.ftype==FType.F_Set:
			return self._get_score_by_sscore(eid, summtids)
		else:
			raise Exception('Unknown FType! self.ftype={{, shoud in {}'.format(self.ftype, [item for item in FType]))

	def _get_score_by_tscore(self, summtids):
		score_list = []
		for tid in summtids:
			tscore = self.tid_tscore_dict.get(tid)
			# print('tid_metric:',tid,tscore)
			if tscore is None:
				raise Exception('Wrong tid! no tscore for tid={}! tscore={}, feature_path={}'.format(tid, tscore, self.fpath))
			score_list.append(tscore)

		score = np.mean(score_list)
		# print('summ:',score,summtids)
		return score

	def _get_score_by_sscore(self, eid, summtids):
		if self.fitem is None: # convert to subclass
			if self.fname=='DoP':
				from f_imp import F_DoP
				self.fitem = F_DoP(self.ds_name, self.fname, self.ftype, self.fpath)
			elif self.fname=='DoV':
				from f_imp import F_DoV
				self.fitem = F_DoV(self.ds_name, self.fname, self.ftype, self.fpath)
			else:
				raise Exception('Undefined summary-level feature! fnmae=%s'%self.fname)
		return self.fitem._get_score_by_sscore(eid, summtids)

	def _read_tscore(self, tf_file): # return tid_tscore_dict
		#print('reading tfeature %s from file: %s'%(self.fname, self.fpath))
		tid_tscore_dict = dict()
		with open(tf_file, 'r', encoding='utf-8') as f:
			for line in f:
				tid, tscore = line.strip().split('\t')
				tid_tscore_dict[int(tid)] = float(tscore)
		return tid_tscore_dict




if __name__ == '__main__':
	# example code 1: get triple-level score for triple-set
	ds_name = 'dbpedia'
	eid = 1
	summtid = [3,4,5,6,7]
	fname = 'GFoV'
	ftype = FType.F_Triple
	fitem = Feature(ds_name, fname, ftype)
	fscore = fitem.get_score(eid, summtid)
	print('fscore:', fscore)
