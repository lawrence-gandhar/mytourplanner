from app.modules import db_operations as dbops
import pandas as pd


class TourCounters:

    def __init__(self, user_id):
        self._user_id = user_id
        self._data = {}

    def process_data(self):
        self._queryset = dbops.fetch_tour_counters(user_id = self._user_id)
        df = pd.DataFrame(self._queryset)
        df.set_index("id", inplace = True)

        planned_tours = len(df[df["travel_start_date"].isnull() == True])
        travelled_tours = len(df[
            (df["travel_start_date"].isnull() == False) &
            (df["travel_end_date"].isnull() == False)
        ])

        on_hold_tours = len(df[
            (df["put_on_hold"].isnull() == True) &
            (df["travel_start_date"].isnull() == True)
        ])

        travel_mode_data = dbops.fetch_travelmode_data()
        tf = pd.DataFrame(travel_mode_data)

        return {
            "planned_tours":planned_tours, 
            "travelled_tours":travelled_tours, 
            "on_hold_tours":on_hold_tours,
            "total_budget": df["budget"].sum() ,
            "total_spent": df["total_spent"].sum(),
            "total_distance": tf["distance"].sum(),
            "highest_budget": df["budget"].max(),
            "lowest_budget": df["budget"].min(),
            "highest_spent": df["total_spent"].max(),
            "lowest_spent": df["total_spent"].min(),
            "longest_travel": tf["distance"].max(),
            "shortest_travel": tf["distance"].min(),
        }
    
    