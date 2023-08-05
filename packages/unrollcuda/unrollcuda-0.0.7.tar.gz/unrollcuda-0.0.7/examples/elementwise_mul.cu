#define MAX_DIMENSIONS 3 // Set the number of dimensions accordingly to your array

__global__ void unroll(
    unsigned int *arr0,
    unsigned int *arr1,
    unsigned int *shape,
    unsigned long long gpu_arr_size,
    unsigned long long shape_total,
    unsigned long long dimensions_count,
    unsigned long long step,
    unsigned char order,
    unsigned long long batch_start    
)
{
    unsigned long long idx = threadIdx.x + blockIdx.x * blockDim.x;
    unsigned long long idx_full;
    unsigned long long i = 0;
    unsigned int indices[MAX_DIMENSIONS];
    unsigned long long tmp;
    
    idx_full = i * step + idx;

    while (idx_full < shape_total && idx_full < gpu_arr_size)
    {
        tmp = idx_full + batch_start; // add batch_start to account for the offset
        // Compute the indices
        for (unsigned int j = 0; j < dimensions_count; ++j)
        {
            unsigned int dimension = (order == 0) ? dimensions_count - j - 1 : j;
            // Modulo by the dimension size
            indices[dimension] = tmp % shape[dimension];
            // Divide by the dimension size
            tmp /= shape[dimension];
        }
        //printf("idx_full: %llu, idx: %llu, batch_start: %llu\n", idx_full, idx, batch_start);
        
        for (unsigned int j = 0; j < dimensions_count; ++j)
        {
            // j is the dimension
            
            // Your code ++
            // Multiply elementwise
            arr0[idx_full] = arr0[idx_full] * arr1[idx_full];
            // Your code --

            break;
        }
        i += 1;
        idx_full = i * step + idx;
    }
    // Free the memory
    delete[] indices;
}
