"""
wrapper to avoid relative path issues when using modules in different folders
"""
import media.plots.food as food

if __name__ == "__main__":
    data, dates = food.get_data()
    data_dict = food.get_counts_from_list(data)
    food.create_cloud(data_dict, "wrapper")