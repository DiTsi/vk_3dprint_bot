from stl import mesh

density = 1.050 # gramm / 1cm^3


def stl_volume(stl_file):
	your_mesh = mesh.Mesh.from_file(stl_file)
	volume, cog, inertia = your_mesh.get_mass_properties()
	volume = volume / 1000  # 1cm^3
	# print('volume = ' + str(volume) + ' cm^3')
	return volume # cm^3


def stl_mass(volume, density):
	mass = volume * density  # gramm
	return mass


