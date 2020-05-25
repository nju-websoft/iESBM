'''
generate iESBM FER files
@file: iesbm_gen.py
@author: qxliu
@time: 2020/5/22 9:47
'''
import argparse
from f_imp import *
def gen_fer(fname, ds_name, topk):
	out_dir = os.path.join(IN_DIR, 'in_ds_fer')
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)
	out_file = os.path.join(out_dir, 'FER_{}_{}_{}.txt'.format(fname, ds_name, topk.name))
	print('output to file:',out_file)
	fpath = None # to use default path
	feature = get_feature_by_name(fname, ds_name, fpath)
	eid_desc_dict = load_eid_desc_tids(ds_name)
	eid_ugold_dict = load_eid_ugold_tids(ds_name, topk)
	eid_list = list(eid_desc_dict.keys())
	eid_list = sorted(eid_list)

	fer_list = []
	line_list = []
	for eid in eid_list:
		#=== 3. get ugold score
		ugold = eid_ugold_dict.get(eid)
		ugscore_list = []
		for uid,gold in ugold.items():
			ugscore = feature.get_score(eid, gold)
			ugscore_list.append(ugscore)
		#=== 2. get edesc score
		# print('ugscore_list:',eid, len(ugscore_list), ugscore_list, np.mean(ugscore_list))
		desctids = eid_desc_dict.get(eid)
		desc_score = feature.get_score(eid, desctids)
		#=== 3. compute fer
		e_fer = np.mean(ugscore_list)/desc_score
		fer_list.append(e_fer)
		line_list.append('{}\t{}\t{}\t{}\n'.format(eid, e_fer,np.mean(ugscore_list),desc_score)) # for debut
		# line_list.append('{}\t{}\n'.format(eid, e_fer))

	#==== compute sig
	fer_sig_with1 = get_sig_with_1(fer_list, with_latex=False) # t, p

	#==== output
	print(fname, ds_name, topk.name,
	      'FER: mean={}, std={}, sigWith1 (t,p)={}'.format(np.mean(fer_list), np.std(fer_list), fer_sig_with1))
	with open(out_file, 'w', encoding='utf-8') as fout:
		fout.writelines(line_list)


def gen_for_default_features():
	ds_list = ['dbpedia','lmdb','dsfaces']
	topk_list = [TOPK.top5, TOPK.top10]
	# fname_list = ['LFoP', 'GFoP', 'GFoV', 'IoPV', 'DoP', 'DoV']
	fname_list = ['GFoP']
	for ds_name in ds_list:
		for topk in topk_list:
			for fname in fname_list:
				gen_fer(fname, ds_name, topk)








if __name__ == '__main__':
	# gen_for_default_features()

	parser = argparse.ArgumentParser(description='iESBM: generate FER files')
	parser.add_argument('feature_name', default=None, type=str, help="Name of the feature, values: 'LFoP', 'GFoP', 'GFoV', 'IoPV', 'DoP' and 'DoV' or name of newly defined feature")
	args = parser.parse_args()

	ds_list = ['dbpedia','lmdb','dsfaces']
	topk_list = [TOPK.top5, TOPK.top10]
	for ds_name in ds_list:
		for topk in topk_list:
			gen_fer(args.feature_name, ds_name, topk)
