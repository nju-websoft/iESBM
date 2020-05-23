'''
implementation of summary-level features
@file: f_imp.py
@author: qxliu
@time: 2020/5/19 11:08
'''
from f_base import *

def get_feature_by_name(fname, ds_name, fpath):
	if fname in ['LFoP', 'GFoP', 'GFoV', 'IoPV']: # default triple-level features
		return Feature(ds_name, fname, FType.F_Triple, fpath)
	elif fname=='DoP':
		return F_DoP(ds_name, fpath=fpath)
	elif fname=='DoV':
		return F_DoV(ds_name, fpath=fpath)
	else:
		cls_name = 'F_%s'%fname
		feature = None
		for cls in Feature.__subclasses__():
			if cls_name==cls.__name__:
				feature = cls(ds_name, fpath=fpath)
				break
		if feature is None:
			raise Exception('Wrong fname! Feature class F_%s undefined for new feature fname=%s'%(fname, fname))







class F_DoP(Feature):
	def __init__(self, ds_name, fname='DoP', ftype=FType.F_Set, fpath=None):
		super().__init__(ds_name, fname, ftype, fpath)
		# self.fpath = os.path.join(ROOT_DIR, 'in', 'in_ds_feature', '{}_{}_tid_propid.txt'.format(self.fname, str(self.ds_name))) if fpath is None else fpath
		self.fpath = os.path.join(IN_DIR, 'in_ds_feature', '{}_{}_tid_propid.txt'.format(self.fname, str(self.ds_name))) if fpath is None else fpath
		self.tid_propid_dict = self._read_sscore(self.fpath)

	def _read_sscore(self, sf_file):
		#print('reading sfeature from file: %s'%sf_file)
		tid_propid_dict = dict()
		with open(sf_file, 'r', encoding='utf-8') as fin:
			for line in fin:
				items = line.strip().split('\t')
				tid = int(items[0].strip())
				propid = int(items[1].strip())
				tid_propid_dict[tid] = propid
		return tid_propid_dict

	def _get_score_by_sscore(self, eid, summtids):
		propid_set = set()
		for tid in summtids:
			propid = self.tid_propid_dict.get(tid)
			propid_set.add(propid)
		dop = len(propid_set)/float(len(set(summtids)))
		# print('eid:',eid,len(propid_set),float(len(set(summtids))))
		return dop


class F_DoV(Feature):
	def __init__(self, ds_name, fname='DoV', ftype=FType.F_Set, fpath=None):
		super().__init__(ds_name, fname, ftype, fpath)
		# self.fpath = os.path.join(ROOT_DIR, 'in', 'in_ds_feature', '{}_{}_tpair_nisub.txt'.format(self.fname, self.ds_name)) if fpath is None else fpath
		self.fpath = os.path.join(IN_DIR, 'in_ds_feature', '{}_{}_tpair_nisub.txt'.format(self.fname, self.ds_name)) if fpath is None else fpath
		self.tpair_nisub_dict = self._read_sscore(self.fpath)

	def _read_sscore(self, sf_file):
		#print('reading sfeature %s from file: %s'%(self.fname, sf_file))
		tpair_nisub_dict = dict()
		with open(sf_file, 'r', encoding='utf-8') as fin:
			for line in fin:
				items = line.strip().split('\t')
				tpair = eval(items[0]) # tuple: (tid-smaller, tid-larger)
				nisub = float(items[1]) # 1-Isub(val(t1), val(t2))
				tpair_nisub_dict[tpair] = nisub
		return tpair_nisub_dict

	def _get_score_by_sscore(self, eid, summtid):
		sorted_summtid = sorted(summtid)
		tnum = len(summtid)
		nisub_sum = 0
		nisub_count = 0
		for i in range(tnum):
			ti = sorted_summtid[i]
			for j in range(i+1, tnum):
				tj = sorted_summtid[j]
				tpair = (ti, tj)
				nisub = self.tpair_nisub_dict.get(tpair)
				if nisub is None:
					raise Exception('Wrong tpair! not exist in tpair_nisub_dict! tpair={}, fpath={}'.format(tpair, self.fpath))
				nisub_sum += nisub
				nisub_count += 1
		dov = float(nisub_sum)/nisub_count if nisub_count>0 else 0
		return dov



if __name__ == '__main__':
	# example code 1: get DoP score of triple-set
	ds_name = 'dbpedia'
	eid = 1
	summtid = [3,4,5,6,7]
	#==== 1.1 call by subclass:
	fdop = F_DoP(ds_name)
	score = fdop.get_score(eid,summtid)
	print('score by sub:',score)
	#==== 1.2. call by super-class (subclass should already registered to Abstract_Feature._get_score_by_sscore()
	fdop = Feature(ds_name, 'DoP', FType.F_Set)
	score = fdop.get_score(eid, summtid)
	print('score by supper:', score)
	# print([cls.__name__ for cls in Abstract_Feature.__subclasses__()])
