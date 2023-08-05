#####################################################.
#     This file stores functions from PREDICT       #
#####################################################.

import os
import sys
import ast
from pathlib import Path
import pandas as pd
import numpy as np
import seaborn as sb
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.inspection import permutation_importance
import shap
from robert.curate import curate
from robert.utils import (
    load_model,
    standardize,
    load_dfs,
    load_database,
    )


def load_test(self, Xy_data, params_df):
    ''''
    Loads Xy data of the test set
    '''

    Xy_test_df = load_database(self, self.args.csv_test, "predict")
    descs_model = ast.literal_eval(params_df['X_descriptors'][0])
    try:
        Xy_data['X_test'] = Xy_test_df[descs_model]
    except KeyError:
        # this might fail if the initial categorical variables have not been transformed
        try:
            self.args.log.write(f"\n   x  There are missing descriptors in the test set! Looking for categorical variables converted from CURATE")
            Xy_test_df = curate.categorical_transform(self,Xy_test_df,'predict')
            Xy_data['X_test'] = Xy_test_df[descs_model]
            self.args.log.write(f"   o  The missing descriptors were successfully created")
        except KeyError:
            self.args.log.write(f"   x  There are still missing descriptors in the test set! The following descriptors are needed: {descs_model}")
            self.args.log.finalize()
            sys.exit()

    if params_df['y'][0] in Xy_test_df:
        Xy_data['y_test'] = Xy_test_df[params_df['y'][0]]
    _, Xy_data['X_test_scaled'] = standardize(self,Xy_data['X_train'],Xy_data['X_test'])

    return Xy_data


def plot_predictions(self, params_dict, Xy_data, path_n_suffix):
    '''
    Plot graphs of predicted vs actual values for train, validation and test sets
    '''

    if params_dict['type'].lower() == 'clas':
        # load the ML model
        loaded_model = load_model(params_dict)
        # Fit the model with the training set
        loaded_model.fit(Xy_data['X_train_scaled'], Xy_data['y_train'])  

    set_types = ['train','valid']
    if 'y_test' in Xy_data:
        set_types.append('test')
    
    graph_style = {'color_train' : 'b',
            'color_valid' : 'orange',
            'color_test' : 'r',
            'dot_size' : 50,
            'alpha' : 1 # from 0 (transparent) to 1 (opaque)
            }

    self.args.log.write(f"\n   o  Saving graphs and CSV databases in:")
    if params_dict['type'].lower() == 'reg':
        _ = graph_reg(self,Xy_data,params_dict,set_types,path_n_suffix,graph_style)

    elif params_dict['type'].lower() == 'clas':
        for set_type in set_types:
            _ = graph_clas(self,loaded_model,Xy_data,params_dict,set_type,path_n_suffix)
    
    return graph_style


def graph_reg(self,Xy_data,params_dict,set_types,path_n_suffix,graph_style):
    '''
    Plot regression graphs of predicted vs actual values for train, validation and test sets
    '''

    # Create graph
    sb.set(style="ticks")
    _, ax = plt.subplots(figsize=(7.45,6))

    # Set styling preferences
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    # Title of the axis
    plt.ylabel(f'Predicted {params_dict["y"]}', fontsize=14)
    plt.xlabel(f'{params_dict["y"]}', fontsize=14)
    
    title_graph = f'Predictions_train_valid'
    if 'test' in set_types:
        title_graph += '_test'
    plt.text(0.5, 1.08, f'{title_graph} of {os.path.basename(path_n_suffix)}', horizontalalignment='center',
        fontsize=14, fontweight='bold', transform = ax.transAxes)

    # Plot the data
    _ = ax.scatter(Xy_data["y_train"], Xy_data["y_pred_train"],
                c = graph_style['color_train'], s = graph_style['dot_size'], edgecolor = 'k', linewidths = 0.8, alpha = graph_style['alpha'], zorder=2)

    _ = ax.scatter(Xy_data["y_valid"], Xy_data["y_pred_valid"],
                c = graph_style['color_valid'], s = graph_style['dot_size'], edgecolor = 'k', linewidths = 0.8, alpha = graph_style['alpha'], zorder=2)
    if 'y_test' in Xy_data:
        _ = ax.scatter(Xy_data["y_test"], Xy_data["y_pred_test"],
                    c = graph_style['color_test'], s = graph_style['dot_size'], edgecolor = 'k', linewidths = 0.8, alpha = graph_style['alpha'], zorder=2)

    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.17),
            fancybox=True, shadow=True, ncol=5, labels=set_types, fontsize=14)

    # Add the regression line with a confidence interval based on the training sets
    Xy_data_df = pd.DataFrame()
    Xy_data_df["y_train"] = Xy_data["y_train"]
    Xy_data_df["y_pred_train"] = Xy_data["y_pred_train"]
    _ = sb.regplot(x="y_train", y="y_pred_train", data=Xy_data_df, scatter=False, color=".1", 
                    truncate = True, ax=ax, seed=params_dict['seed'])

    # Add gridlines
    ax.grid(linestyle='--', linewidth=1)

    # set limits
    min_value_graph, max_value_graph = set_lim_reg(Xy_data,set_types)

    plt.xlim(min_value_graph, max_value_graph)
    plt.ylim(min_value_graph, max_value_graph)

    reg_plot_file = f'{os.path.dirname(path_n_suffix)}/Results_{os.path.basename(path_n_suffix)}.png'
    plt.savefig(f'{reg_plot_file}', dpi=300, bbox_inches='tight')

    path_reduced = '/'.join(f'{reg_plot_file}'.replace('\\','/').split('/')[-2:])
    self.args.log.write(f"      -  Graph in: {path_reduced}")
    plt.clf()


def set_lim_reg(Xy_data,set_types):
    '''
    Set axis limits for regression plots
    '''
    
    size_space = 0.1*abs(min(Xy_data["y_train"])-max(Xy_data["y_train"]))
    min_value_graph = min(Xy_data["y_train"])
    if min(Xy_data["y_valid"]) < min_value_graph:
        min_value_graph = min(Xy_data["y_valid"])
    if 'test' in set_types:
        if min(Xy_data["y_test"]) < min_value_graph:
            min_value_graph = min(Xy_data["y_test"])
    min_value_graph = min_value_graph-size_space
        
    max_value_graph = max(Xy_data["y_train"])
    if max(Xy_data["y_valid"]) > max_value_graph:
        max_value_graph = max(Xy_data["y_valid"])
    if 'test' in set_types:
        if max(Xy_data["y_test"]) > max_value_graph:
            max_value_graph = max(Xy_data["y_test"])
    max_value_graph = max_value_graph+size_space
    
    return min_value_graph, max_value_graph


def graph_clas(self,loaded_model,Xy_data,params_dict,set_type,path_n_suffix):
    '''
    Plot a confusion matrix with the prediction vs actual values
    '''
    
    matrix = ConfusionMatrixDisplay.from_estimator(loaded_model, Xy_data[f'X_{set_type}_scaled'], Xy_data[f'y_{set_type}'], normalize="true", cmap='Blues') 
    matrix.ax_.set_title(f'Confusion Matrix for the {set_type} set of {os.path.basename(path_n_suffix)}', fontsize=14)
    plt.xlabel(f'Predicted {params_dict["y"]}', fontsize=14)
    plt.ylabel(f'{params_dict["y"]}', fontsize=14)
    plt.gcf().axes[0].tick_params(size=14)
    plt.gcf().axes[1].tick_params(size=14)
    clas_plot_file = f'{os.path.dirname(path_n_suffix)}/Results_{os.path.basename(path_n_suffix)}_{set_type}.png'
    plt.savefig(f'{clas_plot_file}', dpi=300, bbox_inches='tight')

    path_reduced = '/'.join(f'{clas_plot_file}'.replace('\\','/').split('/')[-2:])
    self.args.log.write(f"      -  Graph in: {path_reduced}")
    plt.clf()


def save_predictions(self,Xy_data,params_dir):
    '''
    Saves CSV files with the different sets and their predicted results
    '''
    
    Xy_orig_df, Xy_path, params_df, _, _, suffix_title = load_dfs(self,params_dir,'no_print')
    base_csv_name = '_'.join(os.path.basename(Xy_path).replace('.csv','_').split('_')[0:2])
    base_csv_name = f'PREDICT/{base_csv_name}'
    base_csv_path = f"{Path(os.getcwd()).joinpath(base_csv_name)}"
    Xy_orig_train = Xy_orig_df[Xy_orig_df.Set == 'Training']
    Xy_orig_train[f'{params_df["y"][0]}_pred'] = Xy_data['y_pred_train']
    train_path = f'{base_csv_path}_train_{suffix_title}.csv'
    _ = Xy_orig_train.to_csv(train_path, index = None, header=True)
    print_preds = f'      -  Train set with predicted results: {os.path.basename(train_path)}'
    Xy_orig_valid = Xy_orig_df[Xy_orig_df.Set == 'Validation']
    Xy_orig_valid[f'{params_df["y"][0]}_pred'] = Xy_data['y_pred_valid']
    valid_path = f'{base_csv_path}_valid_{suffix_title}.csv'
    _ = Xy_orig_valid.to_csv(valid_path, index = None, header=True)
    print_preds += f'\n      -  Validation set with predicted results: {os.path.basename(valid_path)}'
    if self.args.csv_test != '':
        Xy_orig_test = load_database(self, self.args.csv_test, "no_print")
        Xy_orig_test[f'{params_df["y"][0]}_pred'] = Xy_data['y_pred_test']
        test_path = f'{base_csv_path}_test_{suffix_title}.csv'
        _ = Xy_orig_test.to_csv(test_path, index = None, header=True)
        print_preds += f'\n      -  Test set with predicted results: {os.path.basename(test_path)}'
    self.args.log.write(print_preds)

    path_n_suffix = f'{base_csv_path}_{suffix_title}'

    # store the names of the datapoints
    name_points = {}
    if self.args.names != '':
        if self.args.names.lower() in Xy_orig_train: # accounts for upper/lowercase mismatches
            self.args.names = self.args.names.lower()
        if self.args.names.upper() in Xy_orig_train:
            self.args.names = self.args.names.upper()
        if self.args.names in Xy_orig_train:
            name_points['train'] = Xy_orig_train[self.args.names]
            name_points['valid'] = Xy_orig_valid[self.args.names]
            if self.args.csv_test != '':
                if self.args.names in Xy_orig_test:
                    name_points['test'] = Xy_orig_test[self.args.names]

    return path_n_suffix, name_points


def print_predict(self,Xy_data,params_dict,path_n_suffix):
    '''
    Prints results of the predictions for all the sets
    '''
    
    dat_file = f'{os.path.dirname(path_n_suffix)}/Results_{os.path.basename(path_n_suffix)}.dat'
    path_reduced = '/'.join(f'{dat_file}'.replace('\\','/').split('/')[-2:])
    print_results = f"\n   o  Results saved in {path_reduced}:"
    set_print = 'Train:Validation'

    # get number of points and proportions
    n_train = len(Xy_data['X_train'])
    n_valid = len(Xy_data['X_valid'])
    n_test = 0
    n_points = f'{n_train}:{n_valid}'
    if 'X_test' in Xy_data:
        set_print += ':Test'
        n_test = len(Xy_data['X_test'])
        n_points += f':{n_test}'
    total_points = n_train + n_valid + n_test
    print_results += f"\n      -  Points {set_print} = {n_points}"

    prop_train = round(n_train*100/total_points)
    prop_valid = round(n_valid*100/total_points)
    prop_test = round(n_test*100/total_points)
    prop_print = f'{prop_train}:{prop_valid}'
    if 'X_test' in Xy_data:
        prop_print += f':{prop_test}'
    print_results += f"\n      -  Proportion {set_print} = {prop_print}"
    
    n_descps = len(Xy_data['X_train'].keys())
    print_results += f"\n      -  Number of descriptors = {n_descps}"
    print_results += f"\n      -  Proportion points:descriptors = {n_train+n_valid}:{n_descps}"

    # print results and save dat file
    if params_dict['type'].lower() == 'reg':
        print_results += f"\n      -  Train : R2 = {Xy_data['r2_train']:.2}, MAE = {Xy_data['mae_train']:.2}, RMSE = {Xy_data['rmse_train']:.2}"
        print_results += f"\n      -  Validation : R2 = {Xy_data['r2_valid']:.2}, MAE = {Xy_data['mae_valid']:.2}, RMSE = {Xy_data['rmse_valid']:.2}"
        if 'y_test' in Xy_data:
            print_results += f"\n      -  Test : R2 = {Xy_data['r2_test']:.2}, MAE = {Xy_data['mae_test']:.2}, RMSE = {Xy_data['rmse_test']:.2}"

    elif params_dict['type'].lower() == 'clas':
        print_results += f"\n      -  Train : Accuracy = {Xy_data['acc_train']:.2}, F1 score = {Xy_data['f1_train']:.2}, MCC = {Xy_data['mcc_train']:.2}"
        print_results += f"\n      -  Validation : Accuracy = {Xy_data['acc_valid']:.2}, F1 score = {Xy_data['f1_valid']:.2}, MCC = {Xy_data['mcc_valid']:.2}"
        if 'y_test' in Xy_data:
            print_results += f"\n      -  Test : Accuracy = {Xy_data['acc_test']:.2}, F1 score = {Xy_data['f1_test']:.2}, MCC = {Xy_data['mcc_test']:.2}"

    self.args.log.write(print_results)
    dat_results = open(dat_file, "w")
    dat_results.write(print_results)
    dat_results.close()


def shap_analysis(self,Xy_data,params_dict,path_n_suffix):
    '''
    Plots and prints the results of the SHAP analysis
    '''

    shap_plot_file = f'{os.path.dirname(path_n_suffix)}/SHAP_{os.path.basename(path_n_suffix)}.png'

    # load and fit the ML model
    loaded_model = load_model(params_dict)
    loaded_model.fit(Xy_data['X_train_scaled'], Xy_data['y_train']) 

    # run the SHAP analysis and save the plot
    explainer = shap.Explainer(loaded_model.predict, Xy_data['X_valid_scaled'], seed=params_dict['seed'])
    shap_values = explainer(Xy_data['X_valid_scaled'])

    shap_show = [self.args.shap_show,len(Xy_data['X_valid_scaled'].columns)]
    aspect_shap = 25+((min(shap_show)-2)*5)
    height_shap = 1.2+min(shap_show)/4

    # explainer = shap.TreeExplainer(loaded_model) # in case the standard version doesn't work
    _ = shap.summary_plot(shap_values, Xy_data['X_valid_scaled'], max_display=self.args.shap_show,show=False, plot_size=[7.45,height_shap])

    # set title
    plt.title(f'SHAP analysis of {os.path.basename(path_n_suffix)}', fontsize = 14, fontweight="bold")

    # adjust width of the colorbar
    plt.gcf().axes[-1].set_aspect(aspect_shap)
    plt.gcf().axes[-1].set_box_aspect(aspect_shap)
    
    plt.savefig(f'{shap_plot_file}', dpi=300, bbox_inches='tight')
    plt.clf()
    path_reduced = '/'.join(f'{shap_plot_file}'.replace('\\','/').split('/')[-2:])
    print_shap = f"\n   o  SHAP plot saved in {path_reduced}"

    # collect SHAP values and print
    shap_results_file = f'{os.path.dirname(path_n_suffix)}/SHAP_{os.path.basename(path_n_suffix)}.dat'
    desc_list, min_list, max_list = [],[],[]
    for i,desc in enumerate(Xy_data['X_train_scaled']):
        desc_list.append(desc)
        val_list_indiv= []
        for _,val in enumerate(shap_values.values):
            val_list_indiv.append(val[i])
        min_indiv = min(val_list_indiv)
        max_indiv = max(val_list_indiv)
        min_list.append(min_indiv)
        max_list.append(max_indiv)
    
    if max(max_list, key=abs) > max(min_list, key=abs):
        max_list, min_list, desc_list = (list(t) for t in zip(*sorted(zip(max_list, min_list, desc_list), reverse=True)))
    else:
        min_list, max_list, desc_list = (list(t) for t in zip(*sorted(zip(min_list, max_list, desc_list), reverse=False)))

    path_reduced = '/'.join(f'{shap_results_file}'.replace('\\','/').split('/')[-2:])
    print_shap += f"\n   o  SHAP values saved in {path_reduced}:"
    for i,desc in enumerate(desc_list):
        print_shap += f"\n      -  {desc} = min: {min_list[i]:.2}, max: {max_list[i]:.2}"

    self.args.log.write(print_shap)
    dat_results = open(shap_results_file, "w")
    dat_results.write(print_shap)
    dat_results.close()


def PFI_plot(self,Xy_data,params_dict,path_n_suffix):
    '''
    Plots and prints the results of the PFI analysis
    '''

    pfi_plot_file = f'{os.path.dirname(path_n_suffix)}/PFI_{os.path.basename(path_n_suffix)}.png'

    # load and fit the ML model
    loaded_model = load_model(params_dict)
    loaded_model.fit(Xy_data['X_train_scaled'], Xy_data['y_train']) 

    score_model = loaded_model.score(Xy_data['X_valid_scaled'], Xy_data['y_valid'])
    perm_importance = permutation_importance(loaded_model, Xy_data['X_valid_scaled'], Xy_data['y_valid'], n_repeats=self.args.pfi_epochs, random_state=params_dict['seed'])

    # sort descriptors and results from PFI
    desc_list, PFI_values, PFI_sd = [],[],[]
    for i,desc in enumerate(Xy_data['X_train_scaled']):
        desc_list.append(desc)
        PFI_values.append(perm_importance.importances_mean[i])
        PFI_sd.append(perm_importance.importances_std[i])
        if len(desc_list) == self.args.pfi_show:
            break
  
    PFI_values, PFI_sd, desc_list = (list(t) for t in zip(*sorted(zip(PFI_values, PFI_sd, desc_list), reverse=False)))

    # plot and print results
    fig, ax = plt.subplots(figsize=(7.45,6))
    y_ticks = np.arange(0, len(desc_list))
    ax.barh(desc_list, PFI_values)
    ax.set_yticks(y_ticks,labels=desc_list,fontsize=14)
    plt.text(0.5, 1.08, f'Permutation feature importances (PFIs) of {os.path.basename(path_n_suffix)}', horizontalalignment='center',
        fontsize=14, fontweight='bold', transform = ax.transAxes)
    fig.tight_layout()
    ax.set(ylabel=None, xlabel='PFI')

    plt.savefig(f'{pfi_plot_file}', dpi=300, bbox_inches='tight')
    plt.clf()

    path_reduced = '/'.join(f'{pfi_plot_file}'.replace('\\','/').split('/')[-2:])
    print_PFI = f"\n   o  PFI plot saved in {path_reduced}"

    pfi_results_file = f'{os.path.dirname(path_n_suffix)}/PFI_{os.path.basename(path_n_suffix)}.dat'
    path_reduced = '/'.join(f'{pfi_results_file}'.replace('\\','/').split('/')[-2:])
    print_PFI += f"\n   o  PFI values saved in {path_reduced}:"
    if params_dict['type'].lower() == 'reg':
        print_PFI += f'\n      Original score (from model.score, R2) = {score_model:.2}'
    elif params_dict['type'].lower() == 'clas':
        print_PFI += f'\n      Original score (from model.score, accuracy) = {score_model:.2}'
    # shown from higher to lower values
    PFI_values, PFI_sd, desc_list = (list(t) for t in zip(*sorted(zip(PFI_values, PFI_sd, desc_list), reverse=True)))
    for i,desc in enumerate(desc_list):
        print_PFI += f"\n      -  {desc} = {PFI_values[i]:.2} +- {PFI_sd[i]:.2}"
    
    self.args.log.write(print_PFI)
    dat_results = open(pfi_results_file, "w")
    dat_results.write(print_PFI)
    dat_results.close()


def outlier_plot(self,Xy_data,path_n_suffix,name_points,graph_style):
    '''
    Plots and prints the results of the outlier analysis
    '''

    # detect outliers
    outliers_data, print_outliers = outlier_filter(self, Xy_data, name_points, path_n_suffix)

    # plot data in SD units
    sb.set(style="ticks")
    _, ax = plt.subplots(figsize=(7.45,6))
    plt.text(0.5, 1.08, f'Outlier analysis of {os.path.basename(path_n_suffix)}', horizontalalignment='center',
    fontsize=14, fontweight='bold', transform = ax.transAxes)

    plt.grid(linestyle='--', linewidth=1)
    _ = ax.scatter(outliers_data['train_scaled'], outliers_data['train_scaled'],
            c = graph_style['color_train'], s = graph_style['dot_size'], edgecolor = 'k', linewidths = 0.8, alpha = graph_style['alpha'], zorder=2)
    _ = ax.scatter(outliers_data['valid_scaled'], outliers_data['valid_scaled'],
            c = graph_style['color_valid'], s = graph_style['dot_size'], edgecolor = 'k', linewidths = 0.8, alpha = graph_style['alpha'], zorder=2)
    if 'test_scaled' in outliers_data:
        _ = ax.scatter(outliers_data['test_scaled'], outliers_data['test_scaled'],
            c = graph_style['color_test'], s = graph_style['dot_size'], edgecolor = 'k', linewidths = 0.8, alpha = graph_style['alpha'], zorder=2)
    
    # Set styling preferences and graph limits
    plt.xlabel('SD of the errors',fontsize=14)
    plt.xticks(fontsize=14)
    plt.ylabel('SD of the errors',fontsize=14)
    plt.yticks(fontsize=14)
    
    axis_limit = max(outliers_data['train_scaled'], key=abs)
    if max(outliers_data['valid_scaled'], key=abs) > axis_limit:
        axis_limit = max(outliers_data['valid_scaled'], key=abs)
    if 'test_scaled' in outliers_data:
        if max(outliers_data['test_scaled'], key=abs) > axis_limit:
            axis_limit = max(outliers_data['test_scaled'], key=abs)
    axis_limit = axis_limit+0.5
    plt.ylim(-axis_limit, axis_limit)
    plt.xlim(-axis_limit, axis_limit)

    # plot rectangles in corners
    diff_tvalue = axis_limit - self.args.t_value
    Rectangle_top = mpatches.Rectangle(xy=(axis_limit, axis_limit), width=-diff_tvalue, height=-diff_tvalue, facecolor='grey', alpha=0.3)
    Rectangle_bottom = mpatches.Rectangle(xy=(-(axis_limit), -(axis_limit)), width=diff_tvalue, height=diff_tvalue, facecolor='grey', alpha=0.3)
    ax.add_patch(Rectangle_top)
    ax.add_patch(Rectangle_bottom)

    # save plot and print results
    outliers_plot_file = f'{os.path.dirname(path_n_suffix)}/Outliers_{os.path.basename(path_n_suffix)}.png'
    plt.savefig(f'{outliers_plot_file}', dpi=300, bbox_inches='tight')
    plt.clf()
    path_reduced = '/'.join(f'{outliers_plot_file}'.replace('\\','/').split('/')[-2:])
    print_outliers += f"\n   o  Outliers plot saved in {path_reduced}"

    outlier_results_file = f'{os.path.dirname(path_n_suffix)}/Outliers_{os.path.basename(path_n_suffix)}.dat'
    path_reduced = '/'.join(f'{outlier_results_file}'.replace('\\','/').split('/')[-2:])
    print_outliers += f"\n   o  Outlier values saved in {path_reduced}:"
    if 'train' not in name_points:
        print_outliers += f'\n      x  No names option (or var missing in CSV file)! Outlier names will not be shown'
    else:
        if 'test_scaled' in outliers_data and 'test' not in name_points:
            print_outliers += f'\n      x  No names option (or var missing in CSV file in the test file)! Outlier names will not be shown'

    print_outliers = outlier_analysis(print_outliers,outliers_data,'train')
    print_outliers = outlier_analysis(print_outliers,outliers_data,'valid')
    if 'test_scaled' in outliers_data:
        print_outliers = outlier_analysis(print_outliers,outliers_data,'test')
    
    self.args.log.write(print_outliers)
    dat_results = open(outlier_results_file, "w")
    dat_results.write(print_outliers)
    dat_results.close()


def outlier_analysis(print_outliers,outliers_data,outliers_set):
    '''
    Analyzes the outlier results
    '''
    
    if outliers_set == 'train':
        label_set = 'Train'
        outliers_label = 'outliers_train'
        n_points_label = 'train_scaled'
        outliers_name = 'names_train'
    elif outliers_set == 'valid':
        label_set = 'Validation'
        outliers_label = 'outliers_valid'
        n_points_label = 'valid_scaled'
        outliers_name = 'names_valid'
    elif outliers_set == 'test':
        label_set = 'Test'
        outliers_label = 'outliers_test'
        n_points_label = 'test_scaled'
        outliers_name = 'names_test'

    per_cent = (len(outliers_data[outliers_label])/len(outliers_data[n_points_label]))*100
    print_outliers += f"\n      {label_set}: {len(outliers_data[outliers_label])} outliers out of {len(outliers_data[n_points_label])} datapoints ({per_cent:.1f}%)"
    for val,name in zip(outliers_data[outliers_label], outliers_data[outliers_name]):
        print_outliers += f"\n      -  {name} ({val:.2} SDs)"
    return print_outliers

def outlier_filter(self, Xy_data, name_points, path_n_suffix):
    '''
    Calculates and stores absolute errors in SD units for all the sets
    '''
    
    # calculate absolute errors between predicted y and actual values
    outliers_train = [abs(x-y) for x,y in zip(Xy_data['y_train'],Xy_data['y_pred_train'])]
    outliers_valid = [abs(x-y) for x,y in zip(Xy_data['y_valid'],Xy_data['y_pred_valid'])]
    if 'y_test' in Xy_data:
        outliers_test = [abs(x-y) for x,y in zip(Xy_data['y_test'],Xy_data['y_pred_test'])]

    # the errors are scaled using standard deviation units. When the absolute
    # error is larger than the t-value, the point is considered an outlier
    outliers_mean = np.mean(outliers_train)
    outliers_sd = np.std(outliers_train)

    outliers_data = {}
    outliers_data['train_scaled'] = (outliers_train-outliers_mean)/outliers_sd
    # for some reason, the predictions of the training set in gradient boosting give very small errors.
    # To avoid invalid outlier detections, the code uses the validation deviations instead of the training deviations
    if 'GB_' not in f'{os.path.basename(path_n_suffix)}':
        outliers_data['valid_scaled'] = (outliers_valid-outliers_mean)/outliers_sd
        if 'y_test' in Xy_data:
            outliers_data['test_scaled'] = (outliers_test-outliers_mean)/outliers_sd
    else:
        outliers_mean_valid = np.mean(outliers_valid)
        outliers_sd_valid = np.std(outliers_valid)
        outliers_data['valid_scaled'] = (outliers_valid-outliers_mean_valid)/outliers_sd_valid
        if 'y_test' in Xy_data:
            outliers_data['test_scaled'] = (outliers_test-outliers_mean_valid)/outliers_sd_valid


    print_outliers, naming, naming_test = '', False, False
    if 'train' in name_points:
        naming = True
        if 'test' in name_points:
            naming_test = True

    outliers_data['outliers_train'], outliers_data['names_train'] = detect_outliers(self, outliers_data['train_scaled'], name_points, naming, 'train')
    outliers_data['outliers_valid'], outliers_data['names_valid'] = detect_outliers(self, outliers_data['valid_scaled'], name_points, naming, 'valid')
    if 'y_test' in Xy_data:
        outliers_data['outliers_test'], outliers_data['names_test'] = detect_outliers(self, outliers_data['test_scaled'], name_points, naming_test, 'test')
    
    return outliers_data, print_outliers


def detect_outliers(self, outliers_scaled, name_points, naming_detect, set_type):
    '''
    Detects and store outliers with their corresponding datapoint names
    '''

    val_outliers = []
    name_outliers = []
    if naming_detect:
        name_points_list = name_points[set_type].to_list()
    for i,val in enumerate(outliers_scaled):
        if val > self.args.t_value:
            val_outliers.append(val)
            if naming_detect:
                name_outliers.append(name_points_list[i])

    return val_outliers, name_outliers
