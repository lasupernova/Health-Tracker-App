"""
wrapper to avoid relative path issues when using modules in different folders
"""
import media.plots.food as food

if __name__ == "__main__":
    data, date = food.get_data(user='gabri')
    # data = [unhealthy, cereal, non_vegan, fruits]
    # names = ['unhealthy', 'cereal', 'non_vegan', 'fruits']
    # for data_, name in zip([unhealthy], ['unhealthy']):
    #     print(f">>>{name}")
    # print(unhealthy)
    data_dict = food.get_counts_from_list(data)
    for name, data in data_dict.items():
        food.create_cloud(data, name)