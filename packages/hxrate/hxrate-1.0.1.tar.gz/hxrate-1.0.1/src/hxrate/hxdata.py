import pandas as pd
import numpy as np
import pickle
import os


def load_data_from_hdx_ms_dist(fpath):
    """
    get hdx mass distribution data
    :param fpath: input .csv path for distribution
    :return: timepoints, mass_distribution list
    """

    out_dict = dict()

    mass_dist_list = []

    with open(fpath, 'r') as infile:

        fileread = infile.read().splitlines()

        for ind, line in enumerate(fileread):

            if line.startswith('#'):
                line_chars = line.split(',')
                head_char = line_chars[0].strip('#')
                if head_char == 'tp':
                    out_dict[head_char] = np.array([float(x) for x in line_chars[1:]])
                else:
                    out_dict[head_char] = [x for x in line_chars[1:]]
            else:
                line_chars = line.split(',')
                mass_dist_vals = [float(x) for x in line_chars[1:]]
                mass_dist_list.append(mass_dist_vals)

        infile.close()

    out_dict['mass_dist'] = np.array(mass_dist_list).T

    return out_dict


def write_pickle_object(obj, filepath):
    """
    write an object to a pickle file
    :param obj: object
    :param filepath: pickle file path
    :return: None
    """
    with open(filepath, 'wb') as outfile:
        pickle.dump(obj, outfile)


def load_pickle_object(pickle_fpath):
    """
    load pickle object from pickle file
    :param pickle_fpath: pickle filepath
    :return:
    """
    with open(pickle_fpath, 'rb') as pkfile:
        pkobj = pickle.load(pkfile)
    return pkobj


def write_hx_rate_output(hx_rates, output_path):
    """

    :param hx_rates:
    :param output_path:
    :return: None
    """

    header = 'ind,hx_rate\n'
    data_string = ''

    for ind, hx_rate in enumerate(hx_rates):
        data_string += '{},{}\n'.format(ind, hx_rate)

    with open(output_path, 'w') as outfile:
        outfile.write(header + data_string)
        outfile.close()


def write_hx_rate_output_bayes(hxrate_mean_array,
                               hxrate_median_array,
                               hxrate_std_array,
                               hxrate_5percent_array,
                               hxrate_95percent_array,
                               neff_array,
                               r_hat_array,
                               output_path):

    header = 'ind,rate_mean,rate_median,rate_std,rate_5%,rate_95%,n_eff,r_hat\n'
    data_string = ''

    for num in range(len(hxrate_mean_array)):

        data_string += '{},{},{},{},{},{},{},{}\n'.format(num,
                                                          hxrate_mean_array[num],
                                                          hxrate_median_array[num],
                                                          hxrate_std_array[num],
                                                          hxrate_95percent_array[num],
                                                          hxrate_5percent_array[num],
                                                          neff_array[num],
                                                          r_hat_array[num])

    with open(output_path, 'w') as outfile:
        outfile.write(header + data_string)
        outfile.close()


def write_isotope_dist_timepoints(timepoints, isotope_dist_array, output_path, timepoint_label=None):

    if timepoint_label is None:
        timepoint_label = np.arange(0, len(timepoints))

    tp_label_str = ','.join([str(x) for x in timepoint_label])
    header1 = '#tp_ind,' + tp_label_str + '\n'

    timepoint_str = ','.join(['%.4f' % x for x in timepoints])
    header2 = '#tp,' + timepoint_str + '\n'
    data_string = ''
    for ind, arr in enumerate(isotope_dist_array.T):
        arr_str = ','.join([str(x) for x in arr])
        data_string += '{},{}\n'.format(ind, arr_str)

    with open(output_path, 'w') as outfile:
        outfile.write(header1 + header2 + data_string)
        outfile.close()


def write_backexchange_array(timepoints, backexchange_array, output_path):
    """
    write merged backexchange array
    :param timepoints: timepoints array
    :param backexchange_array: backexchange array
    :param output_path: output path
    :return: Nothing
    """
    header = 'timepoints,backexchange\n'
    data_string = ''
    for tp, backexchange in zip(timepoints, backexchange_array):
        data_string += '{:.4f},{}\n'.format(tp, backexchange)

    with open(output_path, 'w') as outfile:
        outfile.write(header + data_string)
        outfile.close()


def write_backexchange_correction_array(timepoints, backexchange_correction_array, output_path):
    data_string = ''
    header = 'time,avg_dm_rate\n'
    for ind, (time, avg_mass_rate) in enumerate(zip(timepoints, backexchange_correction_array)):
        data_string += '{:.4f},{}\n'.format(time, avg_mass_rate)

    with open(output_path, 'w') as outfile:
        outfile.write(header + data_string)
        outfile.close()


def load_tp_dependent_dict(filepath):
    """
    load the file that has timepoint in first column and a tp dependent variable on second column and outputs a
    dictionary
    :param filepath: filepath
    :return: dictionary
    """
    df = pd.read_csv(filepath)
    timepoints = df.iloc[:, 0].values
    variable_arr = df.iloc[:, 1].values

    out_dict = dict()

    for ind, (tp, var_value) in enumerate(zip(timepoints, variable_arr)):

        out_dict[tp] = var_value

    return out_dict


def make_new_dir(dirpath):

    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    return dirpath


if __name__ == '__main__':

    pass
