var width = 960;
var height = 500;
var svg = d3.select("body")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

var projection = d3.geo.albersUsa()
    .translate([width/2, height/2])
    .scale([1000]);

var path = d3.geo.path()
    .projection(projection);
path.pointRadius(2);

var states = svg.append("g");
var tweets = svg.append("g");

var state_color = d3.scale.quantize()
    .domain([40,60])
    .range(['#ca0020','#f4a582','#92c5de','#0571b0'])

d3.csv("election_results.csv", function(csv){
    d3.json("us-states.json", function(json){
        states.selectAll("path")
            .data(json.features)
            .enter()
            .append("path")
            .attr("d", path)
            .attr("fill", function(d){
                var state = d.properties.NAME;
                for (var i = 0; i < csv.length; i ++){
                    if (csv[i].State == state){
                        console.log(state + " "  + csv[i].State + " " + csv[i].GOP)
                        return state_color(csv[i].Dem)
                    }
                }
            })
            .attr("stroke", "#eee")
    });
});

var tweet_color = d3.scale.linear()
    .range(["blue", "red"])

d3.json("tweets.json", function(json){
    console.log(json.features[1])
    tweets.selectAll("path")
        .data(json.features)
        .enter()
        .append("path")
        .attr("d", path)
        .attr("stroke-width", 1)
        .attr("stroke", "#eee")
        .attr("fill", function(d){
            var sentiment = d.properties.score;
            return tweet_color(sentiment);
        });
});

