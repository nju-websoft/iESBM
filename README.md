# iESBM Benchmark
https://github.com/nju-websoft/iESBM

Last update: 2020-05-20

License: [ODC Attribution License (ODC-By)](https://opendatacommons.org/licenses/by/1-0/index.html)

iESBM: an interpretative Entity Summarization Benchmark on Multiple Datasets.

# Download

* iESBM benchmark: data of iESBM, include datasets, features and FER results, see [iESBM.zip](https://github.com/nju-websoft/iESBM/blob/master/data/iESBM.zip);
* Evaluator (python): code for generating evaluation results (FSR results), see [code/](https://github.com/nju-websoft/iESBM/tree/master/code);
* runs: output files generated by selected entity summarizers and their FSR results, see [runs.zip](https://github.com/nju-websoft/iESBM/blob/master/data/runs.zip).

# Datasets

* <code>ESBM-D</code>: 125 DBpedia entities from [ESBM v1.2](https://w3id.org/esbm/)
* <code>ESBM-L</code>: 50 LinkedMDB entities from [ESBM v1.2](https://w3id.org/esbm/)
* <code>FED</code>: 50 DBpedia entities from [FACES system](http://wiki.knoesis.org/index.php/FACES)

See [in_ds_raw](https://github.com/nju-websoft/iESBM/tree/master/data/in/in_ds_raw)

# Guidelines

## Quick Start
Suppose you want to evaluate your algorithm named 'youralgo', and its summaries generated for entities from the three datasets are in directory 'data/algosumm/youralgo/'.
Run the following command:
<pre>
python iesbm_eval.py -mode FSR -algo_name youralgo
</pre>
Evaluation results will be outputted to directory 'data/out/out_youralgo/'.
See the next section for detailed configurations.

## Evaluate Your Results
The Evaluator can be used to evaluate any general-purpose entity summarizer through the following process:

### Required Input Format
To evaluate your algorithm, please generate summaries for entities from the three datasets and organize the directory of summaries as follows (see [youralgo](https://github.com/nju-websoft/iESBM/tree/master/data/algosumm/youralgo) as example):
<pre>
├── ${algo_name}
│   ├── ${ds_name}
│   │   ├── ${eid}
│   │   │   ├── ${eid}_top5.nt
│   │   │   ├── ${eid}_top10.nt
</pre>
where 
* ${algo_name} is the name of your entity summarization algorithm, e.g. 'relin', 'diversum', 'youralgo';
* ${ds_name} is the alias for dataset, 'dbpedia' for ESBM-D, 'lmdb' for ESBM-L, 'dsfaces' for FED;
* ${eid} is an integer as the unique identifier for each entity, see elist.txt file in each dataset.

### Run the Evaluator
Please put the folder ${algo_name}/ under directory 'data/algosumm/', and run [iesbm_eval.py](https://github.com/nju-websoft/iESBM/blob/master/code/iesbm_eval.py) by the following command:
<pre>
python iesbm_eval.py -algo_name ${algo_name} [-feature_name ${feature_name} -ds_name ${ds_name} -topk ${topk} -mode ${mode}]
</pre>
where parameter <code>-algo_name</code> is necessary when you want to get 'FSR' results of an algorithm, and optional parameters:
 * <code>-feature_name</code> accept values: 'LFoP', 'GFoP', 'GFoV', 'IoPV', 'DoP' and 'DoV';
 * <code>-topk</code> accept two values: 'top5' for k=5 summaries, and 'top10' for k=10 summaries;
 * <code>-mode</code> accept three values: 'FER' for only output FER results, 'FSR' for only output FSR results, and 'all' for output both.

### Output
For each setting (dataset, topk, feature), the evaluator will:

(0) Generate parsed files:

During the preprocesing of summary files, triples in summaries will be converted to triple ids, 
and these ids will be printed files in directory <code>out_${algo_name}/algo_parsed/</code>. 

(1) Generate an output file:

The evaluator will output the evaluation results for summaries to file <code>out_${algo_name}/algo_metrics/${feature_name}\_${ds_name}\_${topk}.txt</code>.
Each line in the file includs the following items (items are seperated by tab):
```
${eid}, ${feature_score}, ${FSR}
```
(2) Print statistical results:
 
Statistical information of the evaluation results will be printed to the concole, including the following items:
```
${feature_name}, ${ds_name}, ${topk}, ${mean_FSR}, ${std_FSR}, ${significance_with_FER}
```
where ${significance_with_FER} composed of two values: t-statistic and p-value of the t-test.
Meanwhile, these results will be outputted to file <code>out_${algo_name}/result_statics_FSR.txt</code>, see [out_youralgo/result_statics_FSR.txt](https://github.com/nju-websoft/iESBM/blob/master/data/out/out_youralgo/result_statics_FSR.txt) as example.

## Add New Feature
You can add customized features to the evaluator according to following process: 
### Add Triple-level Feature
Firstly, compute feature score for each triple in dataset ${ds_name}, and output these information to a file named '${fname}_${ds_name}.txt' (where ${fname} is the name of your new feature, e.g. 'GFoV').
In this file, with each line contains the following items (items are splitted by tab, see [GFoP_dbpedia.txt](https://github.com/nju-websoft/iESBM/blob/master/data/in/in_ds_feature/GFoP_dbpedia.txt) as example):
<pre>
${tid}, ${tscore}
</pre>
Put this file to directory <code>in/in_ds_feature/</code>.

Open [f_imp.py](https://github.com/nju-websoft/iESBM/blob/master/code/f_imp.py), add a new <code>elif</code> statement to the function <code>get_feature_by_name()</code>:
<pre>
elif fname=='${fname}'
    return Feature(ds_name, fname, FType.F_Triple, fpath)
</pre>

Run [iesbm_gen.py](https://github.com/nju-websoft/iESBM/blob/master/code/iesbm_gen.py) to generate FER files for this new feature:
<pre>
python iesbm_gen.py ${fname}
</pre>

Finally, this new feature can be used by setting parameter '-feature ${feature_name}' when running <code>iesbm_eval.py</code>

### Add Summary-level Feature
First, implement a new subclass of <code>f_base.Feature</code> and name this class as 'F_${fname}' (see class F_DoP, F_DoV in [f_imp.py]() as example).
In this class, define the method to get feature score for an entity in function <code>self._get_score_by_sscore()</code>.

Then, open [f_imp.py](https://github.com/nju-websoft/iESBM/blob/master/code/f_imp.py), add a new <code>elif</code>-statement to function <code>get_feature_by_name()</code>, to return an object of the newly defined class:
<pre>
elif fname=='${fname}'
    return F_${fname}(ds_name, fpath=fpath)
</pre>

Run <code>iesbm_gen.py</code> to generate FER files for this new feature:
<pre>
python iesbm_gen.py ${feature_name}
</pre>

Finally, this new feature can be used by setting parameter '-feature ${feature_name}' when running <code>iesbm_eval.py</code>

# Evaluation Results

Effectiveness of existing features (FER), and evaluation results of several selected entity summarizers (FSR) are presented in the following tables. 

You are encouraged to submit the results of your entity summarizer by contacting us. We will add your results to the following tables. Your submission should contain:

* <code>Summary files</code>: summaries generated by your entity summarizer;
* <code>Evaluation results</code>: evaluation results outputted by our evaluator;
* <code>Notes</code>: brief description of your entity summarizer (e.g., name of the summarizer, citation information, parameter settings).

## FER Results

<strong>Table 1. FER on each dataset for k=5.</strong>
<table class="tablesorter" id="tb_fer_top5">
<thead>
<tr><th data-sorter="false" class="header"></th><th class="header">LFoP</th>
<th class="header">GFoP</th>
<th class="header">GFoV</th>
<th class="header">IoPV</th>
<th class="header">DoP</th>
<th class="header">DoV</th>
</tr>
</thead>
<tbody>
<tr>
<td>ESBM-D</td><td>0.561<small>(&#177;0.165)</small>&#8595;</td><td>0.913<small>(&#177;0.052)</small>&#8595;</td><td>0.759<small>(&#177;0.125)</small>&#8595;</td><td>1.275<small>(&#177;0.175)</small>&#8593;</td><td>2.478<small>(&#177;0.747)</small>&#8593;</td><td>1.016<small>(&#177;0.054)</small>&#8593;</td></tr>
<tr>
<td>ESBM-L</td><td>0.581<small>(&#177;0.125)</small>&#8595;</td><td>0.998<small>(&#177;0.029)</small></td><td>1.349<small>(&#177;0.188)</small>&#8593;</td><td>0.864<small>(&#177;0.057)</small>&#8595;</td><td>3.093<small>(&#177;2.394)</small>&#8593;</td><td>1.061<small>(&#177;0.068)</small>&#8593;</td></tr>
<tr>
<td>FED</td><td>0.821<small>(&#177;0.205)</small>&#8595;</td><td>1.012<small>(&#177;0.066)</small></td><td>1.148<small>(&#177;0.153)</small>&#8593;</td><td>0.958<small>(&#177;0.044)</small>&#8595;</td><td>1.699<small>(&#177;0.480)</small>&#8593;</td><td>1.016<small>(&#177;0.046)</small></td></tr>
</tbody></table>
<strong>Table 2. FER on each dataset for k=10.</strong>
<table class="tablesorter" id="tb_fer_top10">
<thead>
<tr><th data-sorter="false" class="header"></th><th class="header">LFoP</th>
<th class="header">GFoP</th>
<th class="header">GFoV</th>
<th class="header">IoPV</th>
<th class="header">DoP</th>
<th class="header">DoV</th>
</tr>
</thead>
<tbody>
<tr>
<td>ESBM-D</td><td>0.569<small>(&#177;0.170)</small>&#8595;</td><td>0.902<small>(&#177;0.048)</small>&#8595;</td><td>0.753<small>(&#177;0.113)</small>&#8595;</td><td>1.267<small>(&#177;0.158)</small>&#8593;</td><td>2.080<small>(&#177;0.555)</small>&#8593;</td><td>1.002<small>(&#177;0.038)</small></td></tr>
<tr>
<td>ESBM-L</td><td>0.757<small>(&#177;0.131)</small>&#8595;</td><td>0.983<small>(&#177;0.025)</small>&#8595;</td><td>1.203<small>(&#177;0.152)</small>&#8593;</td><td>0.917<small>(&#177;0.054)</small>&#8595;</td><td>2.092<small>(&#177;1.298)</small>&#8593;</td><td>1.048<small>(&#177;0.068)</small>&#8593;</td></tr>
<tr>
<td>FED</td><td>0.862<small>(&#177;0.154)</small>&#8595;</td><td>0.993<small>(&#177;0.041)</small></td><td>1.065<small>(&#177;0.098)</small>&#8593;</td><td>0.981<small>(&#177;0.028)</small>&#8595;</td><td>1.601<small>(&#177;0.423)</small>&#8593;</td><td>1.018<small>(&#177;0.029)</small>&#8593;</td></tr>
</tbody></table>



## FSR Results

FSR results for several selected entity summarizers are presented in the following tables. Their output files are also available (runs).

<strong>Table 3. FSR of selected entity summarizers on ESBM-D for k=5.</strong><table class="tablesorter" id="tb_fsr_dbpedia_top5">
<thead>
<tr><th data-sorter="false" class="header"></th><th class="header">LFoP</th>
<th class="header">GFoP</th>
<th class="header">GFoV</th>
<th class="header">IoPV</th>
<th class="header">DoP</th>
<th class="header">DoV</th>
</tr>
</thead>
<tbody>
<tr>
<td>RELIN</td>
<td>0.280<small>(&#177;0.228)</small></td><td>0.869<small>(&#177;0.075)</small></td><td>0.277<small>(&#177;0.098)</small></td><td>1.801<small>(&#177;0.297)</small></td><td>2.351<small>(&#177;0.791)</small>&#8226;</td><td>0.749<small>(&#177;0.253)</small></td></tr>
<tr>
<td>DIVERSUM</td>
<td>0.649<small>(&#177;0.192)</small></td><td>0.910<small>(&#177;0.048)</small>&#8226;</td><td>0.854<small>(&#177;0.167)</small></td><td>1.175<small>(&#177;0.198)</small></td><td>2.753<small>(&#177;0.925)</small></td><td>1.037<small>(&#177;0.086)</small></td></tr>
<!-- <tr>
<td>FACES</td>
<td>0.322<small>(&#177;0.226)</small></td><td>0.849<small>(&#177;0.067)</small></td><td>0.805<small>(&#177;0.184)</small></td><td>1.231<small>(&#177;0.220)</small></td><td>2.664<small>(&#177;0.938)</small></td><td>0.933<small>(&#177;0.245)</small></td></tr> -->
<tr>
<td>FACES-E</td>
<td>0.623<small>(&#177;0.281)</small>&#8226;</td><td>0.914<small>(&#177;0.079)</small>&#8226;</td><td>0.911<small>(&#177;0.208)</small></td><td>1.142<small>(&#177;0.241)</small></td><td>2.494<small>(&#177;0.881)</small>&#8226;</td><td>0.972<small>(&#177;0.118)</small></td></tr>
<tr>
<td>CD</td>
<td>0.334<small>(&#177;0.181)</small></td><td>0.863<small>(&#177;0.062)</small></td><td>0.414<small>(&#177;0.136)</small></td><td>1.620<small>(&#177;0.250)</small></td><td>2.742<small>(&#177;0.886)</small></td><td>1.061<small>(&#177;0.051)</small></td></tr>
<!-- <tr>
<td>LinkSUM</td>
<td>0.350<small>(&#177;0.269)</small></td><td>0.839<small>(&#177;0.091)</small></td><td>0.901<small>(&#177;0.227)</small></td><td>1.147<small>(&#177;0.252)</small></td><td>1.913<small>(&#177;0.609)</small></td><td>0.976<small>(&#177;0.141)</small></td></tr> -->
<tr>
<td>BAFREC</td>
<td>0.585<small>(&#177;0.169)</small>&#8226;</td><td>0.954<small>(&#177;0.056)</small></td><td>0.908<small>(&#177;0.177)</small></td><td>1.117<small>(&#177;0.198)</small></td><td>2.586<small>(&#177;0.755)</small></td><td>0.980<small>(&#177;0.107)</small></td></tr>
<tr>
<td>KAFCA</td>
<td>0.361<small>(&#177;0.248)</small></td><td>0.850<small>(&#177;0.083)</small></td><td>0.646<small>(&#177;0.244)</small></td><td>1.377<small>(&#177;0.294)</small></td><td>2.505<small>(&#177;0.829)</small>&#8226;</td><td>0.993<small>(&#177;0.116)</small>&#8226;</td></tr>
<tr>
<td>MPSUM</td>
<td>0.434<small>(&#177;0.201)</small></td><td>0.876<small>(&#177;0.072)</small></td><td>0.730<small>(&#177;0.250)</small>&#8226;</td><td>1.304<small>(&#177;0.291)</small>&#8226;</td><td>2.742<small>(&#177;0.886)</small></td><td>0.891<small>(&#177;0.187)</small></td></tr>
<tr>
<td>ESA</td>
<td>0.266<small>(&#177;0.212)</small></td><td>0.848<small>(&#177;0.084)</small></td><td>0.529<small>(&#177;0.179)</small></td><td>1.535<small>(&#177;0.282)</small></td><td>2.303<small>(&#177;0.827)</small></td><td>0.930<small>(&#177;0.160)</small></td></tr>
<tr>
<td>DeepLENS</td>
<td>0.302<small>(&#177;0.219)</small></td><td>0.854<small>(&#177;0.076)</small></td><td>0.656<small>(&#177;0.190)</small></td><td>1.407<small>(&#177;0.267)</small></td><td>2.415<small>(&#177;0.801)</small>&#8226;</td><td>0.957<small>(&#177;0.115)</small></td></tr>
</tbody></table>
<strong>Table 4. FSR of selected entity summarizers on ESBM-L for k=5.</strong><table class="tablesorter" id="tb_fsr_lmdb_top5">
<thead>
<tr><th data-sorter="false" class="header"></th><th class="header">LFoP</th>
<th class="header">GFoP</th>
<th class="header">GFoV</th>
<th class="header">IoPV</th>
<th class="header">DoP</th>
<th class="header">DoV</th>
</tr>
</thead>
<tbody>
<tr>
<td>RELIN</td>
<td>0.688<small>(&#177;0.432)</small>&#8226;</td><td>0.991<small>(&#177;0.047)</small>&#8226;</td><td>0.600<small>(&#177;0.137)</small></td><td>1.154<small>(&#177;0.050)</small></td><td>2.775<small>(&#177;2.012)</small>&#8226;</td><td>0.967<small>(&#177;0.189)</small></td></tr>
<tr>
<td>DIVERSUM</td>
<td>0.870<small>(&#177;0.381)</small></td><td>0.993<small>(&#177;0.038)</small>&#8226;</td><td>1.006<small>(&#177;0.247)</small></td><td>0.991<small>(&#177;0.077)</small></td><td>3.869<small>(&#177;3.357)</small></td><td>1.091<small>(&#177;0.075)</small></td></tr>
<!-- <tr>
<td>FACES</td>
<td>0.728<small>(&#177;0.149)</small></td><td>0.953<small>(&#177;0.083)</small></td><td>1.128<small>(&#177;0.466)</small></td><td>0.947<small>(&#177;0.144)</small></td><td>3.869<small>(&#177;3.357)</small></td><td>1.068<small>(&#177;0.134)</small>&#8226;</td></tr> -->
<tr>
<td>FACES-E</td>
<td>0.536<small>(&#177;0.163)</small>&#8226;</td><td>0.962<small>(&#177;0.079)</small></td><td>1.341<small>(&#177;0.296)</small>&#8226;</td><td>0.872<small>(&#177;0.092)</small>&#8226;</td><td>3.848<small>(&#177;3.352)</small></td><td>1.059<small>(&#177;0.103)</small>&#8226;</td></tr>
<tr>
<td>CD</td>
<td>0.470<small>(&#177;0.199)</small></td><td>0.996<small>(&#177;0.073)</small>&#8226;</td><td>1.009<small>(&#177;0.212)</small></td><td>0.959<small>(&#177;0.079)</small></td><td>3.869<small>(&#177;3.357)</small></td><td>1.102<small>(&#177;0.071)</small></td></tr>
<!-- <tr>
<td>LinkSUM</td>
<td>1.026<small>(&#177;0.263)</small></td><td>0.958<small>(&#177;0.056)</small></td><td>1.288<small>(&#177;0.459)</small>&#8226;</td><td>0.894<small>(&#177;0.169)</small>&#8226;</td><td>1.510<small>(&#177;0.648)</small></td><td>0.968<small>(&#177;0.230)</small>&#8226;</td></tr> -->
<tr>
<td>BAFREC</td>
<td>0.562<small>(&#177;0.201)</small>&#8226;</td><td>1.020<small>(&#177;0.053)</small></td><td>1.598<small>(&#177;0.491)</small></td><td>0.781<small>(&#177;0.144)</small></td><td>3.485<small>(&#177;3.228)</small></td><td>1.007<small>(&#177;0.088)</small></td></tr>
<tr>
<td>KAFCA</td>
<td>0.234<small>(&#177;0.200)</small></td><td>0.954<small>(&#177;0.056)</small></td><td>1.309<small>(&#177;0.395)</small>&#8226;</td><td>0.884<small>(&#177;0.108)</small>&#8226;</td><td>3.869<small>(&#177;3.357)</small></td><td>1.104<small>(&#177;0.102)</small></td></tr>
<tr>
<td>MPSUM</td>
<td>0.568<small>(&#177;0.201)</small>&#8226;</td><td>0.979<small>(&#177;0.046)</small></td><td>1.249<small>(&#177;0.428)</small>&#8226;</td><td>0.908<small>(&#177;0.131)</small>&#8226;</td><td>3.869<small>(&#177;3.357)</small></td><td>1.083<small>(&#177;0.104)</small>&#8226;</td></tr>
<tr>
<td>ESA</td>
<td>0.514<small>(&#177;0.235)</small>&#8226;</td><td>1.029<small>(&#177;0.037)</small></td><td>1.241<small>(&#177;0.352)</small>&#8226;</td><td>0.892<small>(&#177;0.116)</small>&#8226;</td><td>3.125<small>(&#177;2.613)</small>&#8226;</td><td>1.013<small>(&#177;0.154)</small>&#8226;</td></tr>
<tr>
<td>DeepLENS</td>
<td>0.361<small>(&#177;0.163)</small></td><td>1.004<small>(&#177;0.037)</small>&#8226;</td><td>1.412<small>(&#177;0.409)</small>&#8226;</td><td>0.840<small>(&#177;0.129)</small>&#8226;</td><td>3.496<small>(&#177;2.343)</small></td><td>1.000<small>(&#177;0.081)</small></td></tr>
</tbody></table>
<strong>Table 5. FSR of selected entity summarizers on FED for k=5.</strong><table class="tablesorter" id="tb_fsr_dsfaces_top5">
<thead>
<tr><th data-sorter="false" class="header"></th><th class="header">LFoP</th>
<th class="header">GFoP</th>
<th class="header">GFoV</th>
<th class="header">IoPV</th>
<th class="header">DoP</th>
<th class="header">DoV</th>
</tr>
</thead>
<tbody>
<tr>
<td>RELIN</td>
<td>0.911<small>(&#177;0.481)</small>&#8226;</td><td>1.028<small>(&#177;0.157)</small>&#8226;</td><td>0.652<small>(&#177;0.329)</small></td><td>1.123<small>(&#177;0.097)</small></td><td>1.473<small>(&#177;0.579)</small></td><td>0.761<small>(&#177;0.209)</small></td></tr>
<tr>
<td>DIVERSUM</td>
<td>1.339<small>(&#177;0.220)</small></td><td>0.962<small>(&#177;0.056)</small></td><td>1.043<small>(&#177;0.191)</small></td><td>0.989<small>(&#177;0.069)</small>&#8226;</td><td>1.783<small>(&#177;0.517)</small></td><td>0.981<small>(&#177;0.097)</small>&#8226;</td></tr>
<tr>
<td>FACES</td>
<td>0.860<small>(&#177;0.314)</small>&#8226;</td><td>0.936<small>(&#177;0.081)</small></td><td>1.489<small>(&#177;0.245)</small></td><td>0.886<small>(&#177;0.084)</small></td><td>1.714<small>(&#177;0.514)</small>&#8226;</td><td>1.019<small>(&#177;0.124)</small>&#8226;</td></tr>
<tr>
<td>FACES-E</td>
<td>0.860<small>(&#177;0.314)</small>&#8226;</td><td>0.936<small>(&#177;0.081)</small></td><td>1.489<small>(&#177;0.245)</small></td><td>0.886<small>(&#177;0.084)</small></td><td>1.714<small>(&#177;0.514)</small>&#8226;</td><td>1.019<small>(&#177;0.124)</small>&#8226;</td></tr>
<tr>
<td>CD</td>
<td>0.799<small>(&#177;0.206)</small>&#8226;</td><td>1.042<small>(&#177;0.075)</small></td><td>0.699<small>(&#177;0.226)</small></td><td>1.118<small>(&#177;0.076)</small></td><td>1.783<small>(&#177;0.517)</small></td><td>1.060<small>(&#177;0.066)</small></td></tr>
<tr>
<td>LinkSUM</td>
<td>0.976<small>(&#177;0.353)</small></td><td>0.987<small>(&#177;0.080)</small>&#8226;</td><td>1.656<small>(&#177;0.250)</small></td><td>0.797<small>(&#177;0.089)</small></td><td>1.460<small>(&#177;0.474)</small></td><td>1.062<small>(&#177;0.074)</small></td></tr>
<tr>
<td>BAFREC</td>
<td>0.928<small>(&#177;0.273)</small></td><td>0.949<small>(&#177;0.078)</small></td><td>1.658<small>(&#177;0.304)</small></td><td>0.811<small>(&#177;0.089)</small></td><td>1.768<small>(&#177;0.516)</small></td><td>0.975<small>(&#177;0.119)</small>&#8226;</td></tr>
<tr>
<td>KAFCA</td>
<td>0.636<small>(&#177;0.248)</small></td><td>0.999<small>(&#177;0.116)</small>&#8226;</td><td>0.864<small>(&#177;0.363)</small></td><td>1.024<small>(&#177;0.092)</small></td><td>1.699<small>(&#177;0.518)</small>&#8226;</td><td>0.909<small>(&#177;0.134)</small></td></tr>
<tr>
<td>MPSUM</td>
<td>0.878<small>(&#177;0.245)</small>&#8226;</td><td>0.918<small>(&#177;0.067)</small></td><td>1.344<small>(&#177;0.289)</small></td><td>0.949<small>(&#177;0.095)</small>&#8226;</td><td>1.783<small>(&#177;0.517)</small></td><td>0.821<small>(&#177;0.225)</small></td></tr>
<tr>
<td>ESA</td>
<td>0.842<small>(&#177;0.323)</small>&#8226;</td><td>1.090<small>(&#177;0.113)</small></td><td>0.813<small>(&#177;0.232)</small></td><td>1.039<small>(&#177;0.075)</small></td><td>1.378<small>(&#177;0.408)</small></td><td>0.875<small>(&#177;0.136)</small></td></tr>
<tr>
<td>DeepLENS</td>
<td>0.823<small>(&#177;0.476)</small>&#8226;</td><td>1.056<small>(&#177;0.095)</small></td><td>1.166<small>(&#177;0.375)</small>&#8226;</td><td>0.926<small>(&#177;0.124)</small>&#8226;</td><td>1.481<small>(&#177;0.486)</small></td><td>0.863<small>(&#177;0.131)</small></td></tr>
</tbody></table>
<strong>Table 6. FSR of selected entity summarizers on ESBM-D for k=10.</strong><table class="tablesorter" id="tb_fsr_dbpedia_top10">
<thead>
<tr><th data-sorter="false" class="header"></th><th class="header">LFoP</th>
<th class="header">GFoP</th>
<th class="header">GFoV</th>
<th class="header">IoPV</th>
<th class="header">DoP</th>
<th class="header">DoV</th>
</tr>
</thead>
<tbody>
<tr>
<td>RELIN</td>
<td>0.392<small>(&#177;0.217)</small></td><td>0.879<small>(&#177;0.063)</small></td><td>0.374<small>(&#177;0.112)</small></td><td>1.655<small>(&#177;0.228)</small></td><td>2.015<small>(&#177;0.627)</small>&#8226;</td><td>0.872<small>(&#177;0.155)</small></td></tr>
<tr>
<td>DIVERSUM</td>
<td>0.413<small>(&#177;0.135)</small></td><td>0.861<small>(&#177;0.048)</small></td><td>0.745<small>(&#177;0.164)</small>&#8226;</td><td>1.299<small>(&#177;0.230)</small>&#8226;</td><td>2.753<small>(&#177;0.925)</small></td><td>1.013<small>(&#177;0.056)</small>&#8226;</td></tr>
<!-- <tr>
<td>FACES</td>
<td>0.301<small>(&#177;0.216)</small></td><td>0.840<small>(&#177;0.067)</small></td><td>0.742<small>(&#177;0.161)</small>&#8226;</td><td>1.299<small>(&#177;0.201)</small>&#8226;</td><td>2.658<small>(&#177;0.923)</small></td><td>0.915<small>(&#177;0.237)</small></td></tr> -->
<tr>
<td>FACES-E</td>
<td>0.516<small>(&#177;0.182)</small></td><td>0.897<small>(&#177;0.053)</small>&#8226;</td><td>0.770<small>(&#177;0.146)</small>&#8226;</td><td>1.270<small>(&#177;0.210)</small>&#8226;</td><td>2.453<small>(&#177;0.842)</small></td><td>0.985<small>(&#177;0.062)</small></td></tr>
<tr>
<td>CD</td>
<td>0.393<small>(&#177;0.155)</small></td><td>0.871<small>(&#177;0.045)</small></td><td>0.555<small>(&#177;0.145)</small></td><td>1.467<small>(&#177;0.219)</small></td><td>2.538<small>(&#177;0.741)</small></td><td>1.026<small>(&#177;0.045)</small></td></tr>
<!-- <tr>
<td>LinkSUM</td>
<td>0.438<small>(&#177;0.300)</small></td><td>0.889<small>(&#177;0.069)</small></td><td>0.751<small>(&#177;0.158)</small>&#8226;</td><td>1.267<small>(&#177;0.191)</small>&#8226;</td><td>1.580<small>(&#177;0.569)</small></td><td>0.937<small>(&#177;0.112)</small></td></tr> -->
<tr>
<td>BAFREC</td>
<td>0.629<small>(&#177;0.191)</small></td><td>0.945<small>(&#177;0.049)</small></td><td>0.850<small>(&#177;0.148)</small></td><td>1.171<small>(&#177;0.181)</small></td><td>1.926<small>(&#177;0.543)</small></td><td>0.968<small>(&#177;0.071)</small></td></tr>
<tr>
<td>KAFCA</td>
<td>0.443<small>(&#177;0.223)</small></td><td>0.883<small>(&#177;0.069)</small></td><td>0.661<small>(&#177;0.195)</small></td><td>1.359<small>(&#177;0.257)</small></td><td>2.199<small>(&#177;0.721)</small></td><td>0.972<small>(&#177;0.065)</small></td></tr>
<tr>
<td>MPSUM</td>
<td>0.405<small>(&#177;0.162)</small></td><td>0.880<small>(&#177;0.060)</small></td><td>0.686<small>(&#177;0.158)</small></td><td>1.349<small>(&#177;0.210)</small></td><td>2.612<small>(&#177;0.765)</small></td><td>0.971<small>(&#177;0.066)</small></td></tr>
<tr>
<td>ESA</td>
<td>0.309<small>(&#177;0.222)</small></td><td>0.839<small>(&#177;0.061)</small></td><td>0.606<small>(&#177;0.149)</small></td><td>1.442<small>(&#177;0.222)</small></td><td>2.088<small>(&#177;0.610)</small>&#8226;</td><td>0.965<small>(&#177;0.082)</small></td></tr>
<tr>
<td>DeepLENS</td>
<td>0.334<small>(&#177;0.209)</small></td><td>0.827<small>(&#177;0.066)</small></td><td>0.674<small>(&#177;0.150)</small></td><td>1.367<small>(&#177;0.207)</small></td><td>2.070<small>(&#177;0.593)</small>&#8226;</td><td>0.994<small>(&#177;0.058)</small>&#8226;</td></tr>
</tbody></table>
<strong>Table 7. FSR of selected entity summarizers on ESBM-L for k=10.</strong><table class="tablesorter" id="tb_fsr_lmdb_top10">
<thead>
<tr><th data-sorter="false" class="header"></th><th class="header">LFoP</th>
<th class="header">GFoP</th>
<th class="header">GFoV</th>
<th class="header">IoPV</th>
<th class="header">DoP</th>
<th class="header">DoV</th>
</tr>
</thead>
<tbody>
<tr>
<td>RELIN</td>
<td>0.865<small>(&#177;0.260)</small></td><td>1.000<small>(&#177;0.040)</small>&#8226;</td><td>0.634<small>(&#177;0.113)</small></td><td>1.143<small>(&#177;0.045)</small></td><td>1.962<small>(&#177;1.646)</small>&#8226;</td><td>0.949<small>(&#177;0.111)</small></td></tr>
<tr>
<td>DIVERSUM</td>
<td>0.570<small>(&#177;0.266)</small></td><td>0.965<small>(&#177;0.040)</small></td><td>1.221<small>(&#177;0.296)</small>&#8226;</td><td>0.922<small>(&#177;0.082)</small>&#8226;</td><td>3.869<small>(&#177;3.357)</small></td><td>1.083<small>(&#177;0.071)</small></td></tr>
<!-- <tr>
<td>FACES</td>
<td>0.730<small>(&#177;0.152)</small>&#8226;</td><td>0.962<small>(&#177;0.074)</small>&#8226;</td><td>0.976<small>(&#177;0.303)</small></td><td>0.994<small>(&#177;0.086)</small></td><td>3.869<small>(&#177;3.357)</small></td><td>1.060<small>(&#177;0.127)</small>&#8226;</td></tr> -->
<tr>
<td>FACES-E</td>
<td>0.470<small>(&#177;0.184)</small></td><td>0.953<small>(&#177;0.051)</small></td><td>1.398<small>(&#177;0.212)</small></td><td>0.867<small>(&#177;0.055)</small></td><td>3.856<small>(&#177;3.353)</small></td><td>1.057<small>(&#177;0.083)</small>&#8226;</td></tr>
<tr>
<td>CD</td>
<td>0.560<small>(&#177;0.171)</small></td><td>0.992<small>(&#177;0.043)</small>&#8226;</td><td>1.302<small>(&#177;0.317)</small>&#8226;</td><td>0.885<small>(&#177;0.100)</small>&#8226;</td><td>2.904<small>(&#177;2.170)</small></td><td>1.077<small>(&#177;0.040)</small></td></tr>
<!-- <tr>
<td>LinkSUM</td>
<td>1.127<small>(&#177;0.172)</small></td><td>0.981<small>(&#177;0.038)</small>&#8226;</td><td>1.042<small>(&#177;0.257)</small></td><td>0.979<small>(&#177;0.100)</small></td><td>1.055<small>(&#177;0.592)</small></td><td>0.879<small>(&#177;0.239)</small></td></tr> -->
<tr>
<td>BAFREC</td>
<td>0.714<small>(&#177;0.146)</small></td><td>1.005<small>(&#177;0.057)</small></td><td>1.360<small>(&#177;0.253)</small></td><td>0.861<small>(&#177;0.074)</small></td><td>2.235<small>(&#177;1.506)</small>&#8226;</td><td>0.937<small>(&#177;0.075)</small></td></tr>
<tr>
<td>KAFCA</td>
<td>0.407<small>(&#177;0.142)</small></td><td>0.969<small>(&#177;0.043)</small></td><td>1.336<small>(&#177;0.337)</small>&#8226;</td><td>0.874<small>(&#177;0.099)</small>&#8226;</td><td>3.119<small>(&#177;2.576)</small></td><td>1.069<small>(&#177;0.065)</small></td></tr>
<tr>
<td>MPSUM</td>
<td>0.564<small>(&#177;0.192)</small></td><td>0.977<small>(&#177;0.031)</small>&#8226;</td><td>1.261<small>(&#177;0.280)</small>&#8226;</td><td>0.909<small>(&#177;0.082)</small>&#8226;</td><td>3.428<small>(&#177;2.898)</small></td><td>1.079<small>(&#177;0.065)</small></td></tr>
<tr>
<td>ESA</td>
<td>0.662<small>(&#177;0.232)</small></td><td>0.993<small>(&#177;0.037)</small>&#8226;</td><td>1.187<small>(&#177;0.207)</small>&#8226;</td><td>0.919<small>(&#177;0.071)</small>&#8226;</td><td>2.257<small>(&#177;1.559)</small>&#8226;</td><td>1.020<small>(&#177;0.082)</small>&#8226;</td></tr>
<tr>
<td>DeepLENS</td>
<td>0.643<small>(&#177;0.188)</small></td><td>0.974<small>(&#177;0.036)</small>&#8226;</td><td>1.210<small>(&#177;0.267)</small>&#8226;</td><td>0.910<small>(&#177;0.087)</small>&#8226;</td><td>2.284<small>(&#177;0.968)</small>&#8226;</td><td>1.061<small>(&#177;0.075)</small>&#8226;</td></tr>
</tbody></table>
<strong>Table 8. FSR of selected entity summarizers on FED for k=10.</strong><table class="tablesorter" id="tb_fsr_dsfaces_top10">
<thead>
<tr><th data-sorter="false" class="header"></th><th class="header">LFoP</th>
<th class="header">GFoP</th>
<th class="header">GFoV</th>
<th class="header">IoPV</th>
<th class="header">DoP</th>
<th class="header">DoV</th>
</tr>
</thead>
<tbody>
<tr>
<td>RELIN</td>
<td>0.883<small>(&#177;0.345)</small>&#8226;</td><td>1.042<small>(&#177;0.089)</small></td><td>0.545<small>(&#177;0.152)</small></td><td>1.151<small>(&#177;0.054)</small></td><td>1.495<small>(&#177;0.505)</small>&#8226;</td><td>0.889<small>(&#177;0.082)</small></td></tr>
<tr>
<td>DIVERSUM</td>
<td>1.021<small>(&#177;0.207)</small></td><td>0.943<small>(&#177;0.050)</small></td><td>1.115<small>(&#177;0.157)</small>&#8226;</td><td>0.978<small>(&#177;0.050)</small>&#8226;</td><td>1.783<small>(&#177;0.517)</small></td><td>1.011<small>(&#177;0.054)</small>&#8226;</td></tr>
<tr>
<td>FACES</td>
<td>0.905<small>(&#177;0.235)</small>&#8226;</td><td>0.928<small>(&#177;0.060)</small></td><td>1.315<small>(&#177;0.219)</small></td><td>0.933<small>(&#177;0.063)</small></td><td>1.584<small>(&#177;0.464)</small>&#8226;</td><td>1.012<small>(&#177;0.055)</small>&#8226;</td></tr>
<tr>
<td>FACES-E</td>
<td>0.905<small>(&#177;0.235)</small>&#8226;</td><td>0.928<small>(&#177;0.060)</small></td><td>1.315<small>(&#177;0.219)</small></td><td>0.933<small>(&#177;0.063)</small></td><td>1.584<small>(&#177;0.464)</small>&#8226;</td><td>1.012<small>(&#177;0.055)</small>&#8226;</td></tr>
<tr>
<td>CD</td>
<td>0.735<small>(&#177;0.175)</small></td><td>1.022<small>(&#177;0.060)</small></td><td>0.840<small>(&#177;0.199)</small></td><td>1.050<small>(&#177;0.063)</small></td><td>1.783<small>(&#177;0.517)</small></td><td>1.055<small>(&#177;0.047)</small></td></tr>
<tr>
<td>LinkSUM</td>
<td>1.028<small>(&#177;0.224)</small></td><td>0.964<small>(&#177;0.061)</small></td><td>1.366<small>(&#177;0.186)</small></td><td>0.893<small>(&#177;0.054)</small></td><td>1.301<small>(&#177;0.337)</small></td><td>1.052<small>(&#177;0.049)</small></td></tr>
<tr>
<td>BAFREC</td>
<td>0.870<small>(&#177;0.181)</small>&#8226;</td><td>0.926<small>(&#177;0.046)</small></td><td>1.433<small>(&#177;0.234)</small></td><td>0.890<small>(&#177;0.064)</small></td><td>1.634<small>(&#177;0.463)</small>&#8226;</td><td>0.998<small>(&#177;0.057)</small>&#8226;</td></tr>
<tr>
<td>KAFCA</td>
<td>0.680<small>(&#177;0.223)</small></td><td>0.984<small>(&#177;0.081)</small>&#8226;</td><td>0.972<small>(&#177;0.246)</small>&#8226;</td><td>0.996<small>(&#177;0.070)</small>&#8226;</td><td>1.624<small>(&#177;0.510)</small>&#8226;</td><td>0.975<small>(&#177;0.078)</small></td></tr>
<tr>
<td>MPSUM</td>
<td>0.804<small>(&#177;0.174)</small></td><td>0.909<small>(&#177;0.051)</small></td><td>1.256<small>(&#177;0.168)</small></td><td>0.954<small>(&#177;0.052)</small></td><td>1.783<small>(&#177;0.517)</small></td><td>0.958<small>(&#177;0.090)</small></td></tr>
<tr>
<td>ESA</td>
<td>0.832<small>(&#177;0.290)</small>&#8226;</td><td>1.047<small>(&#177;0.080)</small></td><td>0.896<small>(&#177;0.183)</small></td><td>1.020<small>(&#177;0.060)</small></td><td>1.292<small>(&#177;0.365)</small></td><td>0.926<small>(&#177;0.080)</small></td></tr>
<tr>
<td>DeepLENS</td>
<td>0.863<small>(&#177;0.377)</small>&#8226;</td><td>0.999<small>(&#177;0.092)</small>&#8226;</td><td>1.116<small>(&#177;0.252)</small>&#8226;</td><td>0.955<small>(&#177;0.077)</small>&#8226;</td><td>1.334<small>(&#177;0.491)</small></td><td>0.908<small>(&#177;0.108)</small></td></tr>
</tbody></table>


# References

<p>
[1] Gong Cheng, Thanh Tran, Yuzhong Qu: RELIN: Relatedness and Informativeness-Based Centrality for Entity Summarization. International Semantic Web Conference (1) 2011: 114-129. <br>
[2] Marcin Sydow, Mariusz Pikula, Ralf Schenkel: The notion of diversity in graphical entity summarisation on semantic knowledge graphs. J. Intell. Inf. Syst. 41(2): 109-149 (2013).<br>
[3] Kalpa Gunaratna, Krishnaprasad Thirunarayan, Amit P. Sheth: FACES: Diversity-Aware Entity Summarization Using Incremental Hierarchical Conceptual Clustering. AAAI 2015: 116-122.<br>
[4] Kalpa Gunaratna, Krishnaprasad Thirunarayan, Amit P. Sheth, Gong Cheng: Gleaning Types for Literals in RDF Triples with Application to Entity Summarization. ESWC 2016: 85-100.<br>
[5] Danyun Xu, Liang Zheng, Yuzhong Qu: CD at ENSEC 2016: Generating Characteristic and Diverse Entity Summaries. SumPre@ESWC 2016.<br>
[6] Andreas Thalhammer, Nelia Lasierra, Achim Rettinger: LinkSUM: Using Link Analysis to Summarize Entity Data. ICWE 2016: 244-261.<br>
[7] Hermann Kroll, Denis Nagel and Wolf-Tilo Balke: BAFREC: Balancing Frequency and Rarity for Entity Characterization in Linked Open Data. EYRE 2018.<br>
[8] Eun-Kyung Kim and Key-Sun Choi: Entity Summarization Based on Formal Concept Analysis. EYRE 2018.<br>
[9] Dongjun Wei, Shiyuan Gao, Yaxin Liu, Zhibing Liu and Longtao Huang: MPSUM: Entity Summarization with Predicate-based Matching. EYRE 2018.<br>
[10] Dongjun Wei, Yaxin Liu, Fuqing Zhu, Liangjun Zhang, Wei Zhou, Jizhong Han and Songlin Hu: ESA: Entity Summarization with Attention. EYRE 2019.<br>
[11] Qingxia Liu, Gong Cheng and Yuzhong Qu: DeepLENS: Deep Learning for Entity Summarization. arXiv preprint 2020. arXiv:2003.03736.<br>
</p>

# Contact
If you have any questions or suggestions, please feel free to contact [Qingxia Liu](http://ws.nju.edu.cn/people/qxliu) and [Gong Cheng](http://ws.nju.edu.cn/~gcheng).



