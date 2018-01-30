import numpy as np
from utils.helpers import moving_average, get_nan_fraction_in_array


def calc_start_of_summer(matrix, start_date):

    start_dates = []

    for index, flow in enumerate(matrix[0]):
        # calculate the percentile which gives the 73 lowest flow days in the second half of the water year
        percentile = np.nanpercentile(matrix[182:len(matrix[:]-1)], 27)
        
        smooth_data = moving_average(matrix[:, index])
        search_range = smooth_data.index(max(smooth_data))

        for data_index, data in enumerate(smooth_data):

            if (data_index >= len(smooth_data) - 4):
                start_dates.append(float('NaN'))
                break
            elif data_index >= search_range and data <= percentile and smooth_data[data_index + 1] <= percentile and \
                smooth_data[data_index + 2] <= percentile and smooth_data[data_index + 3] <= percentile:
                start_dates.append(data_index)
                break
            
    failed_calcs = 0
    for index, dates in enumerate(start_dates):
        if start_dates[index] == search_range:
            start_dates[index] == np.nan
            failed_calcs = failed_calcs + 1
        elif start_dates[index] == 0:
            start_dates[index] == np.nan
            failed_calcs = failed_calcs + 1

    print('Test failed for {} out of {} water years.'.format(failed_calcs, matrix.shape[1]))

        # if get_nan_fraction_in_array(matrix[:, index]) > 0.2:
        #     continue
        # else:
        #     plt.figure(index)
        #     plt.plot(matrix[:, index], '-')
        #     plt.title('Start of Summer Metric')
        #     plt.text(1, max(matrix[:,index])-100, 'Start of Summer: {}'.format(start_dates[index]))
        #     plt.xlabel('Julian Day')
        #     plt.ylabel('Flow, ft^3/s')
        #     plt.axvline(start_dates[index], color='red')
        #     plt.axhline(percentile)
        #     plt.savefig('processedFiles/StartSummer/{}.png'.format(index+1))
    print(start_dates)
    return start_dates
