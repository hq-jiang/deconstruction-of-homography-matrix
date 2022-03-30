import numpy as np

def custom_perspective_transform(img, homography):
    """Custom implementation of perspective transform
    """
    height, width, _ = img.shape
    x = np.arange(width)
    y = np.arange(height)

    grid_x, grid_y = np.meshgrid(x, y)


    grid = np.stack((grid_y, grid_x), axis=2)

    transformed_grid = np.matmul(grid.reshape(-1, 2), homography).reshape((height, width, 2))
    transformed_grid = np.around(transformed_grid).astype(int)

    map_x = transformed_grid[:,:,1]
    map_x = np.where(map_x >= width, width-1, map_x)
    map_x = np.where(map_x < 0, 0, map_x)

    map_y = transformed_grid[:,:,0]
    map_y = np.where(map_y >= height, height-1, map_y)
    map_y = np.where(map_y < 0, 0, map_y)

    transformed_img = img[map_y, map_x]
    return transformed_img
