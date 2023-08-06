import pytest
from datetime import datetime
from turkey_eq import plot_map, retrieve_data

# Тест для функции retrieve_data()
def test_retrieve_data():
    # Подготовка тестовых данных
    file_path = "test_file.h5"
    type_d = "ROTI"
    times = [datetime(2023, 2, 6, 10, 25),
             datetime(2023, 2, 6, 10, 40)]
    
    # Выполнение функции retrieve_data()
    data = retrieve_data(file_path, type_d, times)
    
    # Проверка результатов
    assert len(data) == 2  # Проверяем, что получены данные для двух временных моментов

    # Тест для функции plot_map()
def test_plot_map():
    # Подготовка тестовых данных
    plot_times = [datetime(2023, 2, 6, 10, 25),
                  datetime(2023, 2, 6, 10, 40)]
    data = {"ROTI": {
        datetime(2023, 2, 6, 10, 25): {
            "lat": [37.0, 38.0],
            "lon": [37.0, 38.0],
            "vals": [0.1, 0.2]
        },
        datetime(2023, 2, 6, 10, 40): {
            "lat": [37.0, 38.0],
            "lon": [37.0, 38.0],
            "vals": [0.3, 0.4]
        }
    }}
    type_d = "ROTI"
    lon_limits = (-180, 180)
    lat_limits = (-90, 90)
    nrows = 1
    ncols = 2
    markers = []
    sort = False
    use_alpha = False
    clims = {
        "ROTI": [0, 0.5, "TECu/min"]
    }
    savefig = ""
    
    # Выполнение функции plot_map()
    plot_map(plot_times, data, type_d, lon_limits, lat_limits, nrows, ncols,
             markers, sort, use_alpha, clims, savefig)
    
    # Проверка результатов
    # В данном случае, проверить результаты может быть сложно, 
    # так как функция plot_map() визуализирует данные на графике,
    # поэтому лучше проверить визуально, что график отображается без ошибок.

# Запуск тестов
if __name__ == "__main__":
    pytest.main()
