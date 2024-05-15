from midvoxio.parser import Parser

class filetoarray():
    def get_voxel_data(file):
        parser = Parser(fname=file)
        vox_data = parser.parse()
        return vox_data.voxels[0]
    def get_color_data(file):
        parser = Parser(fname=file)
        vox_data = parser.parse() #materials 
        return vox_data.palettes[0]

# # Initialize the parser with the .vox file path
# parser = Parser(fname='burger.vox')

# # Parse the .vox file to get a Vox object
# vox_data = parser.parse()

# # Debug: Print voxel data
# print("Voxel Data:", vox_data.voxels)

# # Debug: Print palette data
# print("Palette Data:", vox_data.palettes)

# # Convert the Vox object to an array
# vox_array = vox_data.to_list()

# # Debug: Print the resulting array
# print("Voxel Array:", vox_array)