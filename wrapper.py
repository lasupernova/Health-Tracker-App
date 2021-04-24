"""
wrapper to avoid relative path issues when using modules in different folders
"""
import media.plots.food as food

if __name__ == "__main__":
    food.create_cloud('ywb', 'test')