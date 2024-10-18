from flask import (Flask, render_template, 
                   render_template_string, 
                   Response, make_response,
                   request, jsonify)
from Geo_airline import Display_Airline
import json
import logging
from logging.handlers import RotatingFileHandler
import pyecharts


'''
步骤一：配置日志记录器
在 Flask 应用程序中配置日志记录器，可以使用 Python 的内置 logging 模块。
在应用程序的入口文件（app.py）中配置日志记录器：
'''
app = Flask(__name__)

# Configuration logger
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]')
file_handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024, backupCount=10, encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

# Set the log level for the application
app.logger.setLevel(logging.INFO)


@app.route("/")
def index():
    # Get the values from the form
    # start_position = request.form.get('Begin_city')
    # end_position = request.form.get('End_city')
    # print(start_position, end_position)

    # if not start_position:
    #     start_position = '北京'
    # if not end_position:
    #     end_position = '深圳'
    
    # # Call Display_Airline function with custom positions
    # MAP = Display_Airline(start_position, end_position)
    # map_JS = MAP.dump_options()
    
    # # Pass the map options to the template
    # return render_template("index.html", geo_opt=map_JS)
    return render_template("index.html")

# Route to handle map generation
@app.route('/generate_map', methods=['POST'])
def generate_map():
    # Your Python code to generate the map
    # MAP = Display_Airline("北京", "深圳")

    # Retrieve client IP address
    client_ip = request.remote_addr
    app.logger.info(f"Request from client IP address: {client_ip}")

    data = request.get_json()
    begin_city = data.get('begin_city')
    end_city = data.get('end_city')

    # Record user activity
    app.logger.info(f"User requested map from {begin_city} to {end_city}")
    
    if begin_city == '0':
        begin_city = 0
    if end_city == '0':
        end_city = 0
    print(begin_city)
    print(end_city)
    # Render the HTML content from the MAP variable using Jinja2
    # map_html = MAP.render_embed()
    # map_JS = MAP.dump_options_with_quotes()
    # response = make_response(map_html)
    # response.headers['Content-Type'] = 'text/html'
    # print(MAP.dump_options())
    
    try:
        MAP = Display_Airline(begin_city, end_city)
        # Error check
        if MAP:
            map_JS = MAP.dump_options_with_quotes()
            return jsonify(json.loads(map_JS))
        else:
            app.logger.error(f'No such route from {begin_city} to {end_city}!')
            return jsonify({'error': f'No such route from {begin_city} to {end_city}!'})
    except pyecharts.exceptions.NonexistentCoordinatesException as e:
        error_message = str(e)
        app.logger.error(error_message)
        return jsonify({'error': error_message})

if __name__ == '__main__':
    app.run(debug=False)