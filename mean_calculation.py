import saga_helper
import saga_api

import numpy as np
from scipy.stats import ttest_ind




def mean_calculation(name, inp_grid, curve=True):


    no_ls_dir = "E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\Testfiles\\Final_778_random_points_noLS.shp"
    no_ls_shp = saga_api.SG_Get_Data_Manager().Add_Shapes(no_ls_dir)

    ls_dir = "E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\data\\landslides\\all_slides_point.shp"
    ls_shp = saga_api.SG_Get_Data_Manager().Add_Shapes(ls_dir)


    shp_list = [no_ls_shp, ls_shp]

    values = [[], []]


    for j, shp in enumerate(shp_list):

        for i in range(shp.Get_Count()):

            p = shp.Get_Shape_byIndex(i).asPoint()

            punkt = p.Get_Point(i)
            x = punkt.x
            y = punkt.y

            if curve:
                value = inp_grid.Get_Value(x,y)*100
            else:
                value = inp_grid.Get_Value(x,y)

            values[j].append(value)


    saga_api.SG_Get_Data_Manager().Delete(inp_grid)

    saga_api.SG_Get_Data_Manager().Delete(no_ls_shp)
    saga_api.SG_Get_Data_Manager().Delete(ls_shp)


    no_ls_mean = np.mean(values[0])
    ls_mean = np.mean(values[1])

    print(f"\nNoLS-Mean: \n{no_ls_mean} \nLS-Mean: \n{ls_mean}")


    #perform independent two sample t-test
    result = ttest_ind(values[0], values[1])

    print(f"\n{name}:\nP-Value --- {result[1]:.5f}\n\n")


    return 0



if __name__ == "__main__":

    saga_api.SG_UI_ProgressAndMsg_Lock(True)


    # Grid
    gridpfad = f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\slope_grid.sgrd"
    ValueGrid = saga_api.SG_Get_Data_Manager().Add_Grid(gridpfad)
    mean_calculation("Slope", ValueGrid, False)

    gridpfad1 = f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\aspect_grid.sgrd"
    ValueGrid = saga_api.SG_Get_Data_Manager().Add_Grid(gridpfad1)
    mean_calculation("Aspect",ValueGrid, False)

    gridpfad2 = f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\General Curvature.sgrd"
    ValueGrid = saga_api.SG_Get_Data_Manager().Add_Grid(gridpfad2)
    mean_calculation("General Curvature", ValueGrid)

    gridpfad3 = f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\Plan Curvature.sgrd"
    ValueGrid = saga_api.SG_Get_Data_Manager().Add_Grid(gridpfad3)
    mean_calculation("Plan Curvature", ValueGrid)

    gridpfad4 = f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\Profile Curvature.sgrd"
    ValueGrid = saga_api.SG_Get_Data_Manager().Add_Grid(gridpfad4)
    mean_calculation("Profile Curvature", ValueGrid)





