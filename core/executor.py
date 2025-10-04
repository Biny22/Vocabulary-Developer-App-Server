from concurrent.futures import ThreadPoolExecutor
import multiprocessing

# CPU 코어 수의 두 배 설정
max_workers = multiprocessing.cpu_count() * 2
executor = ThreadPoolExecutor(max_workers=max_workers)