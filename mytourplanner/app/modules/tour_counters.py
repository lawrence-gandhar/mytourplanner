from app.modules import db_operations as dbops
import pandas as pd


class TourCounters:

    def __init__(self, user_id):
        self._user_id = user_id
        self._data = {}
        self._queryset = None

        self._get_queryset()
        self._process_data()
        

    def _get_queryset(self):
        self._queryset = dbops.fetch_tour_counters(user_id = self._user_id)

    def _process_data(self):
        df = pd.DataFrame(self._queryset)
        df.set_index("id", inplace = True)
        
        planned_tours = len(df[df["travel_start_date"].isnull() == True])
        travelled_tours = len(df[
            (df["travel_start_date"].isnull() == False) &
            (df["travel_end_date"].isnull() == False)
        ])

        # print(planned_tours, travelled_tours)