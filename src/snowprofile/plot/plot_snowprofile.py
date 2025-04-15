# -*- coding: utf-8 -*-

import snowprofile
import glob
import pandas as pd
import matplotlib.pyplot as plt
from snowtools.plots.stratiprofile import Dictionnaries
from snowtools.plots.stratiprofile.profilPlot import saisonProfil
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import datetime as dt
from matplotlib.patches import Rectangle
import os
import matplotlib



def plot_snowprofile(sp, index_temperature_profiles = 'all', 
                     index_density_profiles = 'all', style_density_profiles = 'step',
                     index_hardness_profiles = 'all', style_hardness_profiles = 'step',
                     index_impurity_profiles = 'all', style_impurity_profiles = 'point',
                     index_ssa_profiles = 'all',  style_ssa_profiles = 'point',
                     index_strength_profiles = 'all', style_strength_profiles = 'point',
                     index_lwc_profiles = 'all', style_lwc_profiles = 'step', 
                     index_scalar_profiles = 'all',
                      **kwargs):
    
    """
    Plot the data (only the vertical property profiles) of a snow profile CAAML.
    Example: plot_snowprofile(sp3, style_density_profiles='step', lw = 2, style_ssa_profiles='step', style_hardness_profiles='step', index_ssa_profiles=[0, 1])
    
    :param sp: SnowProfile object to be plotted
    :type sp: SnowProfile object
    
    :param index_temperature_profiles: index of the temperature profile to be plotted ([0, 2]). Default is 'all', meaning all the temperature profiles will be plotted.
    :type index_temperature_profiles: int
    
    :param index_hardness_profiles: index of the hardness profile to be plotted ([0, 2]). Default is 'all', meaning all the hardness profiles will be plotted.
    :type index_hardness_profiles: int
    :param style_hardness_profiles: plotting option: 'point' to do plot with markers and 'step' to do a step plot (only possible if a thickness is provided). Default is 'step'.
    :type style_hardness_profiles: str
    
    :param index_impurity_profiles: index of the impurity profile to be plotted ([0, 2]). Default is 'all', meaning all the impurity profiles will be plotted.
    :type index_impurity_profiles: int
    :param style_impurity_profiles: plotting option: 'point' to do plot with markers and 'step' to do a step plot (only possible if a thickness is provided). Default is 'point'.
    :type style_impurity_profiles: str

    :param index_ssa_profiles: index of the ssa profile to be plotted ([0, 2]). Default is 'all', meaning all the ssa profiles will be plotted.
    :type index_ssa_profiles: int
    :param style_ssa_profiles: plotting option: 'point' to do plot with markers and 'step' to do a step plot (only possible if a thickness is provided). Default is 'point'.
    :type style_ssa_profiles: str
    
    :param index_strength_profiles: index of the strength profile to be plotted ([0, 2]). Default is 'all', meaning all the strength profiles will be plotted.
    :type index_strength_profiles: int
    :param style_strength_profiles: plotting option: 'point' to do plot with markers and 'step' to do a step plot (only possible if a thickness is provided). Default is 'point'.
    :type style_strength_profiles: str

    :param index_lwc_profiles: index of the lwc profile to be plotted ([0, 2]). Default is 'all', meaning all the lwc profiles will be plotted.
    :type index_lwc_profiles: int
    :param style_lwc_profiles: plotting option: 'point' to do plot with markers and 'step' to do a step plot (only possible if a thickness is provided). Default is 'step'.
    :type style_lwc_profiles: str

    :param index_scalar_profiles: index of the scalar profile to be plotted ([0, 2]). Default is 'all', meaning all the other scalar profiles will be plotted.
    :type index_scalar_profiles: int

    :param index_density_profiles: index of the density profile to be plotted ([0, 2]). Default is 'all', meaning all the density profiles will be plotted.
    :type index_density_profiles: int
    :param style_density_profiles: plotting option: 'point' to do plot with markers and 'step' to do a step plot (only possible if a thickness is provided). Default is 'step'.
    :type style_density_profiles: str
        
    """
    
    
    plt.subplots(figsize = (16,15))
    plt.subplots_adjust(wspace=0.4)
    n_subplots = 1 
            
    if ((not sp.stratigraphy_profile) == False):
        plt.subplot(3,4,n_subplots)
        plot_strati_profile(sp, xlabel = 'Hand hardness', **kwargs)       
        n_subplots+=1
        

    if ((not sp.hardness_profiles) == False) & (index_hardness_profiles is not None):
        plt.subplot(3,4,n_subplots)
        if style_hardness_profiles == 'point':
            plot_point_profile(sp, sp.hardness_profiles, 'hardness', index_hardness_profiles, xlabel = 'Hardness (N)', **kwargs)
        if style_hardness_profiles == 'step':
            plot_step_profile(sp, sp.hardness_profiles, 'hardness', index_hardness_profiles, xlabel = 'Hardness (N)', **kwargs)
        n_subplots+=1
        

    if ((not sp.strength_profiles) == False)  & (index_strength_profiles is not None):
        plt.subplot(3,4,n_subplots)
        if style_strength_profiles == 'point':
            plot_point_profile(sp, sp.strength_profiles, 'strength', index_strength_profiles, xlabel = 'Strength (N)', **kwargs)
        if style_strength_profiles == 'step':
            plot_vline_profile(sp, sp.strength_profiles, 'strength', index_strength_profiles, xlabel = 'Strength (N)', **kwargs)
        n_subplots+=1
        
        
    if ((not sp.temperature_profiles) == False) & (index_temperature_profiles is not None):
        plt.subplot(3,4,n_subplots)
        plot_point_profile(sp, sp.temperature_profiles, 'temperature', index_temperature_profiles, xlabel = 'Temperature (°C)', **kwargs)
        n_subplots+=1
        

    if ((not sp.lwc_profiles) == False)  & (index_lwc_profiles is not None):
        plt.subplot(3,4,n_subplots)
        if style_lwc_profiles == 'point':
            plot_point_profile(sp, sp.lwc_profiles, 'lwc', index_lwc_profiles, xlabel = 'LWC (%)', **kwargs)
        if style_lwc_profiles == 'step':
            plot_vline_profile(sp, sp.lwc_profiles, 'lwc', index_lwc_profiles, xlabel = 'LWC (%)', **kwargs)
        n_subplots+=1

        
    if ((not sp.density_profiles) == False) & (index_density_profiles is not None):
        plt.subplot(3,4,n_subplots)
        if style_density_profiles == 'point':
            plot_point_profile(sp, sp.density_profiles, 'density', index_density_profiles, xlabel = 'Density (kg/m3)', **kwargs)
        if style_density_profiles == 'step':
            plot_vline_profile(sp, sp.density_profiles, 'density', index_density_profiles, xlabel = 'Density (kg/m3)', **kwargs)
        n_subplots+=1
        

    if ((not sp.ssa_profiles) == False)  & (index_ssa_profiles is not None):
        plt.subplot(3,4,n_subplots)
        if style_ssa_profiles == 'point':
            plot_point_profile(sp, sp.ssa_profiles, 'ssa', index_ssa_profiles, xlabel = 'SSA (m2/kg)', **kwargs)
        if style_ssa_profiles == 'step':
            plot_vline_profile(sp, sp.ssa_profiles, 'ssa', index_ssa_profiles, xlabel = 'SSA (m2/kg)', **kwargs)
        n_subplots+=1
        

    if ((not sp.impurity_profiles) == False) & (index_impurity_profiles is not None):
        print('Il y a des impurités')
        plt.subplot(3,4,n_subplots)
        if style_impurity_profiles == 'point':
            plot_point_profile(sp, sp.impurity_profiles, 'mass_fraction', index_impurity_profiles, xlabel = 'Impurity mass fraction', **kwargs)
        if style_impurity_profiles == 'step':
            plot_vline_profile(sp, sp.impurity_profiles, 'mass_fraction', index_impurity_profiles, xlabel = 'Impurity mass fraction', **kwargs)
        n_subplots+=1


    if ((not sp.other_scalar_profiles) == False) & (index_scalar_profiles is not None):
        plt.subplot(3,4,n_subplots)
        plot_point_profile(sp, sp.other_scalar_profiles, 'data', index_scalar_profiles, xlabel = 'Other scalar variable', **kwargs)
        n_subplots+=1
    
    else:
        print('all')



def plot_vline_profile(sp, variable_profiles, name_profile,  index_profiles, xlabel = 'Variable (unit)', ylabel = 'Height (m)', **kwargs):    
    
    colors = iter(plt.cm.tab10(np.linspace(0, 1, 10)))
    if index_profiles != 'all':       # we want to plot the profile with index = [0,1,2]
    
        for i in index_profiles:
            try:
                if 'color' not in kwargs:
                    c = next(colors)
                    plt.vlines(x = variable_profiles[i].data_dict[name_profile], ymin = variable_profiles[i].data_dict['bottom_height'], ymax = variable_profiles[i].data_dict['top_height'], 
                           label = str(i), color = c, **kwargs)
                else:
                    plt.vlines(x = variable_profiles[i].data_dict[name_profile], ymin = variable_profiles[i].data_dict['bottom_height'], ymax = variable_profiles[i].data_dict['top_height'], 
                           label = str(i),  **kwargs)
            except:
                print('A step plot was not possible as no tickness is associated to the data. Plotted using markers.')
                try:
                    height = variable_profiles[i].data_dict['top_height'] - np.divide(variable_profiles[i].data_dict['thickness'], 2.) # to get the height of the middle of each layer
                except:
                    height =  variable_profiles[i].data_dict['height']
                plt.plot(variable_profiles[i].data_dict[name_profile], height, label = str(i) , ls = ':', marker='o', **kwargs)

            
    else:                            # we want to plot all profiles
        for profile in variable_profiles:
            try:    
                print(kwargs)
                if 'color' not in kwargs:
                    c = next(colors)
                    plt.vlines(x = profile.data_dict[name_profile], ymin = profile.data_dict['bottom_height'], ymax = profile.data_dict['top_height'], label = profile.name, color=c, **kwargs)
                else:
                    plt.vlines(x = profile.data_dict[name_profile], ymin = profile.data_dict['bottom_height'], ymax = profile.data_dict['top_height'], label = profile.name, **kwargs)
            except:
                print('A step plot was not possible as no tickness is associated to the data. Plotted using markers.')
                try:
                    height = profile.data_dict['top_height'] - np.divide(profile.data_dict['thickness'], 2.) # to get the height of the middle of each layer
                except:
                    height =  profile.data_dict['height']
        
                plt.plot(profile.data_dict[name_profile], height, label = profile.name , ls = ':', marker='o', **kwargs)
            
                
    plt.xlabel(xlabel)
    plt.grid(ls=':')
    plt.ylabel(ylabel)



def plot_step_profile(sp, variable_profiles, name_profile,  index_profiles, xlabel = 'Variable (unit)', ylabel = 'Height (m)', **kwargs):    
    colors = iter(plt.cm.tab10(np.linspace(0, 1, 10)))
    if index_profiles != 'all':
    
        for i in index_profiles:
            try:
                if 'color' not in kwargs:
                    c = next(colors)
                    plt.step(x = variable_profiles[i].data_dict[name_profile], y = variable_profiles[i].data_dict['top_height'],
                            label = str(i), color = c, **kwargs)
                    plt.vlines(x = variable_profiles[i].data_dict[name_profile][-1], ymax = variable_profiles[i].data_dict['top_height'][-1],
                               ymin = variable_profiles[i].data_dict['bottom_height'][-1], color = c, **kwargs)
                    
                else:
                    plt.step(x = variable_profiles[i].data_dict[name_profile], y = variable_profiles[i].data_dict['top_height'],
                            label = str(i), **kwargs)
                    plt.vlines(x = variable_profiles[i].data_dict[name_profile][-1], ymax = variable_profiles[i].data_dict['top_height'][-1],
                               ymin = variable_profiles[i].data_dict['bottom_height'][-1], **kwargs)
                    
            except:
                print('A step plot was not possible as no tickness is associated to the data. Plotted using markers.')
                try:
                    height = variable_profiles[i].data_dict['top_height'] - np.divide(variable_profiles[i].data_dict['thickness'], 2.) # to get the height of the middle of each layer
                except:
                    height =  variable_profiles[i].data_dict['height']
                plt.plot(variable_profiles[i].data_dict[name_profile], height, label = str(i) , ls = ':', marker='o', **kwargs)

            
    else:
        for profile in variable_profiles:
            try:    
                print(kwargs)
                if 'color' not in kwargs:
                    c = next(colors)
                    plt.step(x = profile.data_dict[name_profile], y = profile.data_dict['top_height'], label = profile.name, color=c, **kwargs)
                    plt.vlines(x = profile.data_dict[name_profile][-1], ymin = profile.data_dict['bottom_height'][-1], ymax = profile.data_dict['top_height'][-1], color=c, **kwargs)
                else:
                    plt.step(x = profile.data_dict[name_profile], y = profile.data_dict['top_height'], label = profile.name, **kwargs)
                    plt.vlines(x = profile.data_dict[name_profile][-1], ymin = profile.data_dict['bottom_height'][-1], ymax = profile.data_dict['top_height'][-1], **kwargs)
            except:
                print('A step plot was not possible as no tickness is associated to the data. Plotted using markers.')
                try:
                    height = profile.data_dict['top_height'] - np.divide(profile.data_dict['thickness'], 2.) # to get the height of the middle of each layer
                except:
                    height =  profile.data_dict['height']
        
                plt.plot(profile.data_dict[name_profile], height, label = profile.name , ls = ':', marker='o', **kwargs)
                           
    plt.xlabel(xlabel)
    plt.grid(ls=':')
    plt.ylabel(ylabel)





def plot_point_profile(sp, variable_profiles, name_profile,  index_profiles, xlabel = 'Variable (unit)', ylabel = 'Height (m)', **kwargs):        
        
    if index_profiles != 'all':
        for i in index_profiles:
            try:
                height = variable_profiles[i].data_dict['top_height'] - np.divide(variable_profiles[i].data_dict['thickness'], 2.) # to get the height of the middle of each layer
                
            except:
                height =  variable_profiles[i].data_dict['height']
            plt.plot(variable_profiles[i].data_dict[name_profile], height, label = str(i) , ls = ':', marker='o', **kwargs)

            
    else:
        for profile in variable_profiles:
            try:
                height = profile.data_dict['top_height'] - np.divide(profile.data_dict['thickness'], 2.) # to get the height of the middle of each layer
                
            except:
                height =  profile.data_dict['height']
        
            plt.plot(profile.data_dict[name_profile], height, label = profile.name , ls = ':', marker='o', **kwargs)
            
                
    plt.xlabel(xlabel)
    plt.grid(ls=':')
    plt.ylabel(ylabel)



def plot_strati_profile(sp, xlabel = 'Hand harness', ylabel = 'Height (m)', **kwargs):

    ax = plt.subplot(3,4,1)
    
    snowiacs=matplotlib.font_manager.findfont('SnowSymbolsIACS')
    snowsymb=matplotlib.font_manager.FontProperties(fname=snowiacs)
    
    coulF1={'PP':'lime','MM':'gold','DF':'forestgreen','RG':'lightpink','FC':'lightblue','DH':'blue','SH':'fuchsia','MF':'red','IF':'cyan','PPhl':'grey', 'PPgp':'lime'}
    convert_type={"PP":"a","DF":"c","RG":"d","FC":"e","DH":"f","MF":"h","IF":"i","SH":"g","PPhl":"o","RGwp":"y", 'PPgp':'a'}
    hardness_convert={'F':1.,'4F':2.,'1F':3.,'P':4.,'K':5.,'I':6.}

    # get data
    height = sp.stratigraphy_profile.data_dict['top_height']
    height.insert(len(height),0)
    hardness = sp.stratigraphy_profile.data_dict['hardness']
    grain1 = sp.stratigraphy_profile.data_dict['grain_1']
    grain2 = sp.stratigraphy_profile.data_dict['grain_2']

    for i in range(len(grain1)):
        c=coulF1[grain1[i]]
        width = hardness_convert[hardness[i]] # width of the rectangle
        delta_h = height[i] - height[i+1] #height of the rectangle
        
        ax.add_patch(Rectangle((0., height[i+1]), width , delta_h, color = c  ))
        
        plt.hlines(y=height[i+1], xmin=0, xmax=width, linewidth=1, color='k')
        plt.hlines(y=height[i], xmin=0, xmax=width, linewidth=1, color='k')
        
        plt.text(width/2 -0.45, height[i+1] + delta_h/2 - 0.01, convert_type[grain1[i]] + convert_type[grain2[i]], fontproperties=snowsymb,fontsize=12, color='k', fontweight='bold')
        
    ax.set_xlim(xmax=6)
    plt.xlabel(xlabel)
    plt.grid(ls=':')
    plt.ylabel(ylabel)
    tick_hardness_str=["F","4F","1F", 'P', 'K', 'I']
    tick_hardness_nb=[1,2,3, 4, 5, 6]
    ax.set_xticks(tick_hardness_nb) # Set the tick positions
    ax.set_xticklabels(tick_hardness_str) # Set the tick labels
