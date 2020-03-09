###
# Google Hash Code Online Qualification Round 2017
# This code aims at solving the problem in Qualification Round 2017
# The problem is about Streaming Videos.
#
# Author: Teki Chan
# Date: 14 Feb 2020
###
import sys

def read_file(in_file):
    """
    Read Intput File

    Args:
        in_file: input file path

    Returns:
        no_of_caches: Number of cache servers
        , cache_size:   Each cache server's size
        , video_sizes:  List of video sizes
        , ep_dc_latencies:  List of latency between Endpoint and Data Center
        , ep_no_of_caches:  List of Number of connected Cache Servers in each Endpoint
        , ep_cache_latencies:   List of each endpoint's latency to a connected cache server
        , video_ep_requests:    Dict of requests of each video from each Endpoint
    """
    no_of_videos = 0
    no_of_endpoints = 0
    no_of_request_desc = 0
    no_of_caches = 0
    cache_size = 0      # Each cache server's size
    video_sizes = []    # List of video sizes
    ep_dc_latencies = []    # List of latency between Endpoint and Data Center
    ep_no_of_caches = []    # List of Number of connected Cache Servers in each Endpoint

    # list of each endpoint's latency to a connected cache server
    # [{cache_idx: latency, 0: 100, 1: 150, ...}, ...]
    ep_cache_latencies = []

    # dict of requests of each video from each endpoint
    # {(video_idx, endpoint_idx): no_of_requests), (3, 0): 1500, (0, 1): 1200, ...}
    video_ep_requests = {}

    # Read the file into variables    
    with open(in_file, 'r') as infile:
        # Process lines and save data into variables
        no_of_videos, no_of_endpoints, no_of_request_desc, no_of_caches, cache_size = [int(x) for x in infile.readline().strip().split(' ')]
        video_sizes = [int(x) for x in infile.readline().strip().split(' ')]

        for ep_idx in range(0, no_of_endpoints):
            ep_dc_latency, no_of_connect_caches = [int(x) for x in infile.readline().strip().split(' ')]
            ep_dc_latencies.append(ep_dc_latency)

            ep_cache_latency = {}
            for cache_cnt in range(0, no_of_connect_caches):
                cache_idx, cache_latency = [int(x) for x in infile.readline().strip().split(' ')]
                ep_cache_latency[cache_idx] = cache_latency
            ep_no_of_caches.append(no_of_connect_caches)
            ep_cache_latencies.append(ep_cache_latency)

        for request_cnt in range(0, no_of_request_desc):
            [video_idx, ep_idx, request_size] = [int(x) for x in infile.readline().strip().split(' ')]
            video_ep_requests[(video_idx, ep_idx)] = request_size

    '''
    print(no_of_videos)
    print(no_of_endpoints)
    print(no_of_request_desc)
    print(no_of_caches)
    print(cache_size)
    print(video_sizes)
    print(ep_dc_latencies)
    print(ep_no_of_caches)
    print(ep_cache_latencies)
    print(video_ep_requests)
    '''

    return no_of_caches, cache_size, video_sizes, ep_dc_latencies, ep_no_of_caches, ep_cache_latencies, video_ep_requests   # return essential variables

def process(no_of_caches, cache_size, video_sizes, ep_dc_latencies, ep_no_of_caches, ep_cache_latencies, video_ep_requests):
    """
    The main program reads the input file, processes the calculation
    and writes the output file.
    The target is to max(sum(requests x (dc_latency - ep_latency))).
    The score is sum(requests x (dc_latency - ep_latency)) / sum(requests) x 1000.

    Args:
        no_of_caches: Number of cache servers
        cache_size:   Each cache server's size
        video_sizes:  List of video sizes
        ep_dc_latencies:  List of latency between Endpoint and Data Center
        ep_no_of_caches:  List of Number of connected Cache Servers in each Endpoint
        ep_cache_latencies:   List of each endpoint's latency to a connected cache server
        video_ep_requests:    Dict of requests of each video from each Endpoint    
    Returns:
        Sum of Saved Time by cache servers. That is the score.
        , Dict of cache index with list of video lists. That is the result.
    """
    # define result data structure: {cache_idx: [video_ix, ...], ...}
    result = {}
    # total used size in each cache: {cache_idx: used_size, ...}
    cache_used_sizes = {}
    # Calculate saved time
    # sum(requests x (dc_latency - ep_latency)) / sum(requests) x 1000
    score = 0
    sum_saved_time = 0  # sum(requests x (dc_latency - ep_latency))
    sum_requests = sum([requests for requests in video_ep_requests.values()])    # sum(requests)

    # sort endpoints by requests
    '''
    ep_requests_dict = {}
    for video_ep, requests in video_ep_requests.items():
        ep_idx = video_ep[1]
        if ep_idx in ep_requests_dict:
            ep_requests_dict[ep_idx] += requests
        else:
            ep_requests_dict[ep_idx] = requests
    ep_list = []
    for ep_idx, subtotal_requests in ep_requests_dict.items():
        if len(ep_list) == 0 or subtotal_requests <= ep_requests_dict[ep_list[-1]]:
            ep_list.append(ep_idx)
        else:
            for _idx, saved_ep_idx in enumerate(ep_list):
                if subtotal_requests > ep_requests_dict[saved_ep_idx]:
                    ep_list.insert(_idx, ep_idx)
                    break
    '''

    # for each endpoint:
    # for ep_idx in ep_list:
    #    ep_cache_latency = ep_cache_latencies[ep_idx]
    for ep_idx, ep_cache_latency in enumerate(ep_cache_latencies):
        # skip if no latency can save
        if len(ep_cache_latency) == 0:
            continue

        # list each saved latency by cache server
        cache_index_list = []
        latency_list = []
        for cache_index, latency in ep_cache_latency.items():
            if len(latency_list) == 0 or latency >= latency_list[-1]:
                cache_index_list.append(cache_index)
                latency_list.append(latency)
            else:
                for _pos, _latency in enumerate(latency_list):
                    if latency < _latency:
                        cache_index_list.insert(_pos, cache_index)
                        latency_list.insert(_pos, latency)
                        break              

        '''
        print(cache_index_list)
        print(latency_list)
        '''

        # sort each video by requests descendingly
        video_index_list = []
        request_list = []
        for video_idx_ep_idx, requests in video_ep_requests.items():
            if video_idx_ep_idx[1] == ep_idx:
                if len(request_list) == 0 or requests <= request_list[-1]:
                    video_index_list.append(video_idx_ep_idx[0])
                    request_list.append(requests)
                else:
                    for _pos, _requests in enumerate(request_list):
                        if requests > _requests:
                            video_index_list.insert(_pos, video_idx_ep_idx[0])
                            request_list.insert(_pos, requests) 
                            break                     

        '''
        print(video_index_list)
        print(request_list)
        '''

        # put the larger request into faster saved latency until cache is full
        for video_pos, video_index in enumerate(video_index_list):
            for cache_pos, cache_index in enumerate(cache_index_list):
                if cache_index not in result:
                    result[cache_index] = [video_index]
                    cache_used_sizes[cache_index] = video_sizes[video_index]
                    # calculate score
                    sum_saved_time += request_list[video_pos] * (ep_dc_latencies[ep_idx] - latency_list[cache_pos])
                    break
                elif video_index in result[cache_index]:
                    # calculate score
                    sum_saved_time += request_list[video_pos] * (ep_dc_latencies[ep_idx] - latency_list[cache_pos])
                    break   # Video already exists in a faster cache
                else:
                    # Check if cache is full
                    if cache_used_sizes[cache_index] + video_sizes[video_index] <= cache_size:
                        result[cache_index].append(video_index)
                        cache_used_sizes[cache_index] += video_sizes[video_index]
                        # calculate score
                        sum_saved_time += request_list[video_pos] * (ep_dc_latencies[ep_idx] - latency_list[cache_pos])
                        break

    # calculate score
    '''
    print(sum_saved_time)
    print(sum_requests)
    '''
    score = (sum_saved_time / sum_requests) * 1000.0

    return score, result   # return process result

def write_file(out_file, cache_video_list):
    """
    Write the submission file

    Args:
        out_file: output file path
        cache_video_list: the dict of each cache with list of videos
    """
    with open(out_file, 'w') as outfile:
        outfile.write('{}\n'.format(len(cache_video_list)))
        for cache_idx in cache_video_list:
            outfile.write('{} {}\n'.format(
                cache_idx
                , ' '.join([str(s) for s in cache_video_list[cache_idx]]))
            )

def main(in_file, out_file):
    no_of_caches, cache_size, video_sizes, ep_dc_latencies, ep_no_of_caches, ep_cache_latencies, video_ep_requests = read_file(in_file)
    saved_times, cache_video_list = process(no_of_caches, cache_size, video_sizes, ep_dc_latencies, ep_no_of_caches, ep_cache_latencies, video_ep_requests)
    print('Score: {}'.format(saved_times))
    # print(cache_video_list)
    if out_file is not None:
        write_file(out_file, cache_video_list)
        print('{} is saved. The program completed.'.format(out_file))
    else:
        print('The program completed.')

if __name__ == "__main__":
    # Check arguments
    if len(sys.argv) < 2:
        print(sys.argv[0] + ' [in file] [out file: optional]')
    elif len(sys.argv) == 2:
        main(sys.argv[1], None)
    else:
        main(sys.argv[1], sys.argv[2])