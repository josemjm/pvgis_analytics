# -*- coding: utf-8 -*-
# Author: José María Jiménez Manzano

## https://leimao.github.io/blog/Python-tqdm-Multiprocessing/
## https://kirk86.github.io/2017/08/python-multiprocessing/

from multiprocessing import Pool

from tqdm import tqdm


def run_map_multiprocessing(func, argument_list, num_processes):
    pool = Pool(processes=num_processes)

    pool.map(func=func, iterable=argument_list)
    pool.close()
    pool.join()

    return


def run_imap_multiprocessing(func, argument_list, num_processes):
    pool = Pool(processes=num_processes)

    result_list_tqdm = []
    for result in tqdm(pool.imap(func=func, iterable=argument_list), total=len(argument_list)):
        result_list_tqdm.append(result)

    return result_list_tqdm


def run_imap_unordered_multiprocessing(func, argument_list, num_processes):
    pool = Pool(processes=num_processes)

    result_list_tqdm = []
    for result in tqdm(pool.imap_unordered(func=func, iterable=argument_list), total=len(argument_list)):
        result_list_tqdm.append(result)

    return result_list_tqdm


def run_apply_async_multiprocessing(func, argument_list, num_processes):
    pool = Pool(processes=num_processes)

    jobs = [
        pool.apply_async(func=func, args=(*argument,))
        if isinstance(argument, tuple)
        else pool.apply_async(func=func, args=(argument,))
        for argument in argument_list
    ]
    pool.close()
    result_list_tqdm = []
    for job in tqdm(jobs):
        result_list_tqdm.append(job.get())

    return result_list_tqdm
