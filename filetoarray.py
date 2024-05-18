from midvoxio.parser import Parser
from voxypy.models import Entity
from midvoxio.voxio import vox_to_arr

class filetoarray():
    def get_size(file):
        return(vox_to_arr(file).shape)
    def get_voxel_data(file):
        parser = Parser(fname=file)
        vox_data = parser.parse()
        return vox_data.voxels[0]
    def get_color_data(file):
        entity = Entity().from_file(file)
        return entity.get_palette(padded=True)
    def get_full_voxel_data(file):
        voxel_data = filetoarray.get_voxel_data(file)
        palette_data = filetoarray.get_color_data(file)
        color_map = {idx: color for idx, color in enumerate(palette_data)}
        voxel_colors = [(x, y, z, color_map[color_index]) for x, y, z, color_index in voxel_data]
        return voxel_colors
    def layer_based_voxel_data(file):
        entity = Entity().from_file(file)
        return entity.get_dense()
