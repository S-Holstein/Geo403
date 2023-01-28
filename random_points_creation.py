import saga_helper
import saga_api
import os



def Run_Create_Random_Points( number=50):

    Tool = saga_api.SG_Get_Tool_Library_Manager().Get_Tool('shapes_points', '21')
    if Tool == None:
        print('Failed to create tool: Create Random Points')
        return False

    # for b in range(shps_range_new):
    shp_file = "E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\Testfiles\\union_tracks_buffer.shp"

    loaded_shp = saga_api.SG_Get_Data_Manager().Add_Shapes(shp_file)

    Tool.Reset()

    Tool.Set_Parameter('EXTENT', '3')
    Tool.Set_Parameter('POLYGONS', loaded_shp)
    Tool.Set_Parameter('COUNT', number)
    Tool.Set_Parameter('DISTRIBUTE', 'all polygons')
    Tool.Set_Parameter('ITERATIONS', 1000)
    Tool.Set_Parameter('DISTANCE', 0.000000)

    if Tool.Execute() == False:
        print('failed to execute tool: ' + Tool.Get_Name().c_str())
        return False

    #_____________________________________
    # Save results to file:
    # Path = os.path.split(File)[0] + os.sep

    Data = Tool.Get_Parameter('POINTS').asDataObject()
    Data.Save("E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\Testfiles\\temp_random_points.shp")

    #_____________________________________
    saga_api.SG_Get_Data_Manager().Delete(loaded_shp)

    return True




def random_points_generator(demanded_points):

    # Grid
    gridpfad = f"E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\converted_viewshed\\w001001.sgrd"
    ValueGrid = saga_api.SG_Get_Data_Manager().Add_Grid(gridpfad)

    value_count = 0
    value_coordinates = []
    value_list = []


    while value_count < demanded_points:


        Run_Create_Random_Points()


        temp_dir = "E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\Testfiles\\temp_random_points.shp"
        loaded = saga_api.SG_Get_Data_Manager().Add_Shapes(temp_dir)


        for i in range(loaded.Get_Count()):

            a = loaded.Get_Shape_byIndex(i).asPoint()

            punkt = a.Get_Point(i)
            x = punkt.x
            y = punkt.y

            value = ValueGrid.Get_Value(x,y)


            if value != -32768 and value != 0.0:

                if punkt not in value_coordinates:       # -1 because of dismissing the water shp file

                    value_list.append(value)
                    value_coordinates.append(punkt)   # -1 because of dismissing the water shp file
                    value_count = len(value_list)     # -1 because of dismissing the water shp file

        saga_api.SG_Get_Data_Manager().Delete(loaded)

        # saga_api.SG_Get_Data_Manager().Delete(GRID)

    print(value_count)

    Run_Create_New_Shapes_Layer(value_coordinates)

    return True



def Run_Create_New_Shapes_Layer(value_coordinates):

    Tool = saga_api.SG_Get_Tool_Library_Manager().Get_Tool('shapes_tools', '0')
    if Tool == None:
        print('Failed to create tool: Create New Shapes Layer')
        return False


    Tool.Reset()

    Tool.Set_Parameter('NAME', 'Final')
    Tool.Set_Parameter('TYPE', 'Point')
    Tool.Set_Parameter('VERTEX', 'x, y')
    Tool.Set_Parameter('NFIELDS', 2)
    Tool.Set_Parameter('FIELDS.NAME0', 'ID')
    Tool.Set_Parameter('FIELDS.TYPE0', 'unsigned 1 byte integer')
    Tool.Set_Parameter('FIELDS.NAME1', 'Name')
    Tool.Set_Parameter('FIELDS.TYPE1', 'string')

    if Tool.Execute() == False:
        print('failed to execute tool: ' + Tool.Get_Name().c_str())
        return False


    # Save results to file:
    Data = Tool.Get_Parameter('SHAPES').asDataObject()


    for i, coordinate in enumerate(value_coordinates):

        if i >= 778:
            continue

        Data.asShapes().Add_Shape().Add_Point(coordinate.x, coordinate.y)

    Data.Save("E:\\Uni_Kurs_Envs\\Geo403\\DATEN\\NEW\\Testfiles" + os.sep + Data.Get_Name() + f'_778_random_points_noLS.shp')

    #_____________________________________
    # saga_api.SG_Get_Data_Manager().Delete_All() # job is done, free memory resources

    return True


if __name__ == "__main__":

    saga_api.SG_UI_ProgressAndMsg_Lock(True)

    random_points_generator(778)
