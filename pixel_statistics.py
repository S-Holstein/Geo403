import numpy as np
from time import perf_counter

import saga_helper
import saga_api
import matplotlib.pyplot as plt

import asyncio



def slope_plot(viewshed, landslide):

    X = ["0°-10°", "10°-20°", "20°-30°", "30°-40°", "40°+"]

    X_axis = np.arange(len(X))

    plt.grid()

    plt.bar(X_axis - 0.2, viewshed[1], 0.4, label = 'Viewshed')
    plt.bar(X_axis + 0.2, landslide[1], 0.4, label = 'Landslide')


    plt.xticks(X_axis, X)
    plt.xlabel("Hangneigungsklassen", weight="bold")
    plt.ylabel("Pixelanzahl [%]", weight="bold")
    plt.title("Hangneigung/Slope", weight="bold", fontsize=18)
    plt.legend()
    plt.savefig(f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\Plots\\slope", dpi=180)
    plt.close()



def aspect_plot(viewshed, landslide):

    X = ["0°-45°", "45°-90°", "90°-135°", "135°-180°", "180°-225°", "225°-270°", "270°-315°", "315°+"]

    X_axis = np.arange(len(X))

    fig, ax = plt.subplots()

    ax.grid()

    ax.bar(X_axis - 0.2, viewshed[1], 0.4, label = 'Viewshed')
    ax.bar(X_axis + 0.2, landslide[1], 0.4, label = 'Landslide')

    fig.autofmt_xdate()

    ax.set_xticks(X_axis, X)
    ax.set_xlabel("Grad°", weight="bold")
    ax.set_ylabel("Pixelanzahl [%]", weight="bold")
    ax.set_title("Exposition/Aspect", weight="bold", fontsize=18)
    ax.legend()
    fig.savefig(f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\Plots\\aspect", dpi=180)
    plt.close()



def curv_plot(viewshed, landslide, curv_type):

    X = ["<-1", "-1 - -0.5", "-0.5 - 0", "0 - 0.5", "0.5 - 1", ">1"]

    X_axis = np.arange(len(X))

    fig, ax = plt.subplots()

    ax.grid()

    ax.bar(X_axis - 0.2, viewshed[1], 0.4, label = 'Viewshed')
    ax.bar(X_axis + 0.2, landslide[1], 0.4, label = 'Landslide')

    fig.autofmt_xdate()

    ax.set_xticks(X_axis, X)
    ax.set_xlabel("Krümmungsklasse", weight="bold")
    ax.set_ylabel("Pixelanzahl [%]", weight="bold")
    ax.set_title(f"{curv_type} Krümmung", weight="bold", fontsize=18)
    ax.legend()
    fig.savefig(f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\Plots\\{curv_type}_curvature", dpi=180)
    plt.close()



def slope(inp_grid):

    count = 0

    counter_list = [0,0,0,0,0]


    for cell in range(inp_grid.Get_NCells()):

        value = inp_grid.asDouble(cell)



        if value != -9999.0:

            count += 1

            if value <= 10:

                counter_list[0] += 1

            elif 10 < value <= 20:

                counter_list[1] += 1


            elif 20 < value <= 30:

                counter_list[2] += 1


            elif 30 < value <= 40:

                counter_list[3] += 1

            else:

                counter_list[4] += 1

    relative_count_list = [
        round((counter_list[0]/count)*100, 2),
        round((counter_list[1]/count)*100, 2),
        round((counter_list[2]/count)*100, 2),
        round((counter_list[3]/count)*100, 2),
        round((counter_list[4]/count)*100, 2)]

    # print(count)
    # print(counter_list)

    saga_api.SG_Get_Data_Manager().Delete(inp_grid)

    return counter_list, relative_count_list, count



def aspect(inp_grid):

    count = 0

    counter_list = [0, 0, 0, 0, 0, 0, 0, 0]


    for cell in range(inp_grid.Get_NCells()):

        value = inp_grid.asDouble(cell)


        if value != -99999.0:

            count += 1

            if value <= 0.785398125:

                counter_list[0] += 1

            elif 0.785398125 < value <= 1.57079625:

                counter_list[1] += 1

            elif 1.57079625 < value <= 2.356194375:

                counter_list[2] += 1

            elif 2.356194375 < value <= 3.1415925:

                counter_list[3] += 1

            elif 3.1415925 < value <= 3.926990625:

                counter_list[4] += 1

            elif 3.926990625 < value <= 4.71238875:

                counter_list[5] += 1

            elif 4.71238875 < value <= 5.497786875:

                counter_list[6] += 1

            else:

                counter_list[7] += 1

    relative_count_list = [
        round((counter_list[0]/count)*100, 2),
        round((counter_list[1]/count)*100, 2),
        round((counter_list[2]/count)*100, 2),
        round((counter_list[3]/count)*100, 2),
        round((counter_list[4]/count)*100, 2),
        round((counter_list[5]/count)*100, 2),
        round((counter_list[6]/count)*100, 2),
        round((counter_list[7]/count)*100, 2)
    ]

    # print(count)
    # print(counter_list)

    saga_api.SG_Get_Data_Manager().Delete(inp_grid)

    return counter_list, relative_count_list, count



def curvature(inp_grid):

    count = 0

    counter_list = [0, 0, 0, 0, 0, 0]


    for cell in range(inp_grid.Get_NCells()):

        raw_value = inp_grid.asDouble(cell)

        # Maßeinheit anpassen
        value = raw_value * 100

        if raw_value != -99999.0 and raw_value != 0.0:

            count += 1

            if value <= -1:

                counter_list[0] += 1

            elif -1 < value <= -0.5:

                counter_list[1] += 1

            elif -0.5 < value <= 0:

                counter_list[2] += 1

            elif 0 < value <= 0.5:

                counter_list[3] += 1

            elif 0.5 < value <= 1:

                counter_list[4] += 1

            else:

                counter_list[5] += 1

    relative_count_list = [
        round((counter_list[0]/count)*100, 2),
        round((counter_list[1]/count)*100, 2),
        round((counter_list[2]/count)*100, 2),
        round((counter_list[3]/count)*100, 2),
        round((counter_list[4]/count)*100, 2),
        round((counter_list[5]/count)*100, 2),
    ]

    # print(count)
    # print(counter_list)

    saga_api.SG_Get_Data_Manager().Delete(inp_grid)

    return counter_list, relative_count_list, count



def main():

    # Slope
    gridpfad_slope = f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\slope_grid.sgrd"
    slope_grid = saga_api.SG_Get_Data_Manager().Add_Grid(gridpfad_slope)

    viewshed_slope = slope(slope_grid)

    gridpfad_clipped_slope = f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\clipped_slope_grid.sgrd"
    clipped_slope_grid = saga_api.SG_Get_Data_Manager().Add_Grid(gridpfad_clipped_slope)

    landslide_slope = slope(clipped_slope_grid)

    # Ergebnisse plotten
    slope_plot(viewshed_slope, landslide_slope)



    # Aspect
    gridpfad_aspect = f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\Aspect_grid.sgrd"
    aspect_grid = saga_api.SG_Get_Data_Manager().Add_Grid(gridpfad_aspect)

    viewshed_aspect = aspect(aspect_grid)

    gridpfad_clipped_aspect = f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\clipped_Aspect_grid.sgrd"
    clipped_aspect_grid = saga_api.SG_Get_Data_Manager().Add_Grid(gridpfad_clipped_aspect)

    landslide_aspect = aspect(clipped_aspect_grid)

    # Ergebnisse plotten
    aspect_plot(viewshed_aspect, landslide_aspect)



    # Generel curvature
    gridpfad_gen_curv = f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\General_Curvature_grid.sgrd"
    gen_curv_grid = saga_api.SG_Get_Data_Manager().Add_Grid(gridpfad_gen_curv)

    viewshed_gen_curv = curvature(gen_curv_grid)

    gridpfad_clipped_gen_curv = f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\clipped_General_Curvature_grid.sgrd"
    clipped_gen_curv_grid = saga_api.SG_Get_Data_Manager().Add_Grid(gridpfad_clipped_gen_curv)

    landslide_gen_curv = curvature(clipped_gen_curv_grid)

    # Ergebnisse plotten
    curv_plot(viewshed_gen_curv, landslide_gen_curv, "Generelle")



    # plan curvature
    gridpfad_plan_curv = f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\Plan_Curvature_grid.sgrd"
    plan_curv_grid = saga_api.SG_Get_Data_Manager().Add_Grid(gridpfad_plan_curv)

    viewshed_plan_curv = curvature(plan_curv_grid)

    gridpfad_clipped_plan_curv = f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\clipped_Plan_Curvature_grid.sgrd"
    clipped_plan_curv_grid = saga_api.SG_Get_Data_Manager().Add_Grid(gridpfad_clipped_plan_curv)

    landslide_plan_curv = curvature(clipped_plan_curv_grid)

    # Ergebnisse plotten
    curv_plot(viewshed_plan_curv, landslide_plan_curv, "Plan")



    # profile curvature
    gridpfad_profile_curv = f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\Profile_Curvature_grid.sgrd"
    profile_curv_grid = saga_api.SG_Get_Data_Manager().Add_Grid(gridpfad_profile_curv)

    viewshed_profile_curv = curvature(profile_curv_grid)

    gridpfad_clipped_profile_curv = f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\clipped_Profile_Curvature_grid.sgrd"
    clipped_profile_curv_grid = saga_api.SG_Get_Data_Manager().Add_Grid(gridpfad_clipped_profile_curv)

    landslide_profile_curv = curvature(clipped_profile_curv_grid)

    # Ergebnisse plotten
    curv_plot(viewshed_profile_curv, landslide_profile_curv, "Profil")


    return 0



if __name__ == "__main__":

    start_t = perf_counter()

    saga_api.SG_UI_ProgressAndMsg_Lock(True)

    main()

    end_t = perf_counter()

    print(f"Duration: {end_t - start_t}")






