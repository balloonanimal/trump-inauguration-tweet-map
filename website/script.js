var width = 1200;
var height = 700;
var svg = d3.select("body")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

var projection = d3.geo.albersUsa()
    .translate([width/2, height/2])
    .scale([1500]);

var path = d3.geo.path()
    .projection(projection);
path.pointRadius(3);

var states = svg.append("g");
var tweets = svg.append("g");
var div = d3.select("body")
    .append("div")
    .attr("class", "popup")
    .attr("opacity", 0);

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
            .attr("stroke", "#eeeeee")
            .attr("stroke-width", 2)
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
        .attr("stroke-width", 1.5)
        .attr("stroke", "#eeeeee")
        .attr("fill", function(d){
            var sentiment = d.properties.score;
            return tweet_color(sentiment);
        })
        .on("mouseover", function(d){
            div.transition()
                .duration(200)
                .style("opacity", 0.9);
            div.text(d.properties.text)
                .style("left", (d3.event.pageX) + "px")     
                .style("top", (d3.event.pageY - 28) + "px");
        })
        .on("mouseout", function(d) {       
            div.transition()        
                .duration(500)      
                .style("opacity", 0);  
        })
});

