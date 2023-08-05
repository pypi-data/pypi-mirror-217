import numpy as np
import dask.array as da
import dask
import unrollcuda_test as uc
from pycuda import gpuarray
import time

"""def get_random_array(dimensions, start, end, dtype):
    # mean and standard deviation, based on start and end values
    mu, sigma = (start+end)/2, (end-start)/6
    shape = [int(size) for size in dimensions]
    arr = np.random.normal(mu, sigma, shape)
    arr = np.clip(arr, start, end)
    arr = arr.astype(dtype)
    return arr"""

def get_random_array(dimensions, start, end, dtype):
    # mean and standard deviation, based on start and end values
    mu, sigma = (start+end)/2, (end-start)/6
    shape = [int(size) for size in dimensions]
    # Create the dask array
    arr = da.random.normal(mu, sigma, size=shape, chunks=(1000, 1000, 1000))  # Adjust chunks based on your system's memory
    arr = da.clip(arr, start, end)
    arr = arr.astype(dtype)
    return arr.compute()


def call_unroll(
        self, 
        **kwargs
        ):
    # Reshape the array to 1D
    # gpu_arr1 = kwargs['arr1'].reshape(-1, order=self.reshape_order)
    with dask.config.set(**{'array.slicing.split_large_chunks': True}):
        gpu_arr1 = kwargs['arr1'].reshape(-1)
    # We need to split array the same way as the original array
    gpu_arr1 = gpu_arr1[
            self.batch_start:self.batch_start+self.batch_size
            ]
    # Send the array to GPU
    # gpu_arr1 = gpuarray.to_gpu(gpu_arr1.compute())
    gpu_arr1 = gpuarray.to_gpu(gpu_arr1)
    self.log('self.block: '+str(self.block))
    self.log('self.grid: '+str(self.grid))
    # Call the kernel with the additiona array
    self.unroll(
        self.gpu_arr, 
        gpu_arr1, 
        self.gpu_shape,
        self.gpu_arr_size, 
        self.arr_size, 
        self.len_shape, 
        self.step, 
        self.reshape_order_gpu,
        self.batch_start_gpu, 
        block=self.block,
        grid=self.grid
        )
    

def main():
    start_time = time.time()
    dimensions = [2000, 1000, 1000]
    print('Generating array 0')
    arr0 = get_random_array(dimensions, 0, 10, np.uint32)
    # print(arr0)
    print('Generating array 1')
    arr1 = get_random_array(dimensions, 0, 10, np.uint32)
    # print(arr1)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Data preparation time: '+str(elapsed_time))
    
    # Read the kernel code from the file
    with open('elementwise_mul.cu', 'r') as f:
        kernel_code = f.read()
    
    # Define the unrollcuda instance
    ker = uc.kernel(kernel_code, verbose=True, max_block_x=0, batch_size=0)
    
    # Redefine the call_unroll method
    ker.call_unroll = call_unroll
    
    # Call inference with the new additional parameter
    start_time = time.time()
    arr_new = ker.inference(arr0, arr1=arr1).compute()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Cuda time: '+str(elapsed_time))
    
    # Check if the result is correct
    start_time = time.time()
    arr_new_check = np.multiply(arr0, arr1)
    # Check equality of the two arrays
    print(np.array_equal(arr_new, arr_new_check))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Numpy time: '+str(elapsed_time))


if __name__ == '__main__':
    main()
