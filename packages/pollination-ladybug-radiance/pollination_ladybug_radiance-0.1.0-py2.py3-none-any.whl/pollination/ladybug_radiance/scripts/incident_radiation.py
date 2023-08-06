if __name__ == '__main__':
    import math
    import pathlib
    import json
    from ladybug.viewsphere import view_sphere
    from ladybug.analysisperiod import AnalysisPeriod
    from ladybug_radiance.skymatrix import SkyMatrix
    from ladybug_radiance.intersection import intersection_matrix

    from ladybug_geometry.geometry3d import Mesh3D

    def evaluate_boolean(value):
        if value == 'true' or value == 'True' or value is True:
            return True
        else:
            return False

    # map function inputs to script
    north = {{self.north}}
    high_sky_density = evaluate_boolean('{{self.high_sky_density}}')
    ground_reflectance = {{self.ground_reflectance}}
    avg_irr = evaluate_boolean('{{self.average_irradiance}}')
    use_benefit = evaluate_boolean('{{self.radiation_benefit}}')
    bal_temp = {{self.balance_temp}}
    offset_dist = {{self.offset_dist}}
    run_period = AnalysisPeriod.from_string('{{self.run_period}}')

    # load geometry
    context_file = pathlib.Path('context_geo.json')
    geometry_file = pathlib.Path('input_geo.json')

    input_geo = json.loads(geometry_file.read_text())
    study_mesh = Mesh3D.from_dict(input_geo)

    context_geo = []
    if context_file.is_file():
        context_data = json.loads(context_file.read_text())
        context_geo = [Mesh3D.from_dict(context_data)]

    # compute sky matrix
    hoys = None if len(run_period) == 8760 else run_period.hoys
    if use_benefit:
        sky_matrix = SkyMatrix.from_epw_benefit(
            'weather.epw', bal_temp, 2, hoys,
            north, high_sky_density, ground_reflectance
        )
    else:
        sky_matrix = SkyMatrix.from_epw(
            'weather.epw', hoys, north, high_sky_density
        )
    # get the direct and diffuse radiation values
    dir_vals, diff_vals = sky_matrix.direct_values, sky_matrix.diffuse_values
    if avg_irr:  # compute the radiation values into irradiance
        conversion = 1000 / sky_matrix.wea_duration
        dir_vals = tuple(v * conversion for v in dir_vals)
        diff_vals = tuple(v * conversion for v in diff_vals)
    # return the session state variable for the sky sphere values
    total_sky_rad = [dir_rad + dif_rad for dir_rad, dif_rad in zip(dir_vals, diff_vals)]
    ground_value = (sum(total_sky_rad) / len(total_sky_rad)) * ground_reflectance
    ground_rad = [ground_value] * len(total_sky_rad)
    sky_mtx = total_sky_rad + ground_rad

    high_res = False if len(sky_mtx) == 290 else True
    # run intersections
    lb_vecs = view_sphere.reinhart_dome_vectors if high_res \
        else view_sphere.tregenza_dome_vectors
    if north != 0:
        north_angle = math.radians(north)
        lb_vecs = tuple(vec.rotate_xy(north_angle) for vec in lb_vecs)
    lb_grnd_vecs = tuple(vec.reverse() for vec in lb_vecs)
    vectors = lb_vecs + lb_grnd_vecs
    # compute the intersection matrix
    int_mtx = intersection_matrix(
        vectors, study_mesh.face_centroids, study_mesh.face_normals, context_geo,
        offset_dist, True
    )
    # calculate final results
    values = [
        str(sum(r * w for r, w in zip(pt_rel, sky_mtx)))
        for pt_rel in int_mtx
    ]
    with open('results.txt', 'w') as outf:
        outf.write('\n'.join(values))
