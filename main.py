# import libs
from core.libs import *
from flask import Flask, request, json
from core.mysql import Mysql_Connect
import configs

app = Flask(__name__)

# modules
db = Mysql_Connect(configs.host, configs.login, configs.password, configs.db_name)

# variables
address = "0.0.0.0"
port = 5000

# dict with options(sql injection defence)
dict_prices = {
    "200000":200000,
    "400000":400000,
    "600000":600000,
    "800000":800000,
    "1000000":1000000,
    "1200000":1200000,
    "1400000":1400000,
    "1600000":1600000,
    "1800000":1800000,
    "2000000":2000000,
    "2200000":2200000,
    "2400000":2400000,
    "2600000":2600000,
    "2800000":2800000,
    "3000000":3000000
}

dict_years = {
    "1900":1900,
    "1910":1910,
    "1920":1920,
    "1930":1930,
    "1940":1940,
    "1950":1950,
    "1960":1960,
    "1970":1970,
    "1980":1980,
    "1990":1990,
    "2000":2000,
    "2010":2010,
    "2020":2020,
}

dict_sell_period = {
    "15" : 15,
    "30" : 30,
    "60" : 60,
}

# refirect all routes and allow get, post requests
@app.route('/', defaults={'path': '/'})
@app.route('/<path:path>', methods=['GET'])

# catch all requests
def catch_all(path):
    if path.lower() == "api":
        # array with available props for security
        available_props = [
            "sell_period",
            "build_year",
            "price",
        ]
        # sql request
        sql_request = ""
        
        try:
            # loop for checking properties
            for arg in request.args:

                # check for property is available
                if arg.lower() in available_props:
                    if arg.lower() == "build_year":
                        if sql_request == "":
                            sql_request += "SELECT * FROM houses WHERE %s >= %d" % (arg, int(request.args[arg]))
                        else:
                            sql_request += " AND %s >= %d" % (arg, int(request.args[arg]))
                    else:
                        if sql_request == "":
                            sql_request += "SELECT * FROM houses WHERE %s <= %d" % (arg, int(request.args[arg]))
                        else:
                            sql_request += " AND %s <= %d" % (arg, int(request.args[arg]))
                else:
                    continue


            # add sorting
            sql_request += " ORDER BY price"
            data_array = db.Read(sql_request)
            # get headers
            describe_array = list(map(lambda data: data[0],db.Read("DESCRIBE houses")))
            
            # variable for houses
            houeses_array = list(map(lambda house: dict(zip(describe_array, house)), data_array))

            # return data
            return json.dumps(houeses_array)
            
            # # if some error
        except:
            return "Request data is not correct. Check request data!"
        
    else:
        # preparing data
        template_root = open("./src/index.html", "r").read()
        template_item = open("./src/item.html", "r").read()

        # variables for search in database
        price = Int_From_Dict(Str_From_Dict("price" ,request.args), dict_prices)
        year = Int_From_Dict(Str_From_Dict("year" ,request.args), dict_years)
        sell_period = Int_From_Dict(Str_From_Dict("sell_period" ,request.args), dict_sell_period)

        # create sql request
        sql_request = "SELECT * FROM houses WHERE price <= %d AND build_year >= %d" % (price, year)

        # add sell period to sql request
        if sell_period != -1:
            sql_request += " AND sell_period <= %d" % sell_period
        
        # add sortering
        sql_request += " ORDER BY price"

        # load data from db
        db_response = db.Read(sql_request)

        # create content
        content = ""

        # main loop
        for record in db_response:
            # variables
            item = template_item

            # loop for parameters
            for number in range(len(record)):
                item = item.replace("!!%d!!" % (number), str(record[number]))
            
            # add to contant
            content += item

        # create page
        template = template_root.replace("!!CONTENT!!", str(content))
        return template

# start app
if __name__ == '__main__':
    app.run(address, port, True)

