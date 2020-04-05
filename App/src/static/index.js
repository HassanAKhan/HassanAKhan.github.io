function openNav() {
    document.getElementById("mySidepanel").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidepanel").style.width = "0";
}

function render(response) {
    var mpnet = JSON.parse(response);
    var color = d3.scale.category20();
    var svg_layer = [];
    var node_layer = [];
    var link_layer = [];
    var layer_label = [];
    var intra_svg = []
    var intra_link = [];

    // Calculate size for the figure
    // var width = Math.sqrt(mpnet.nodes.length) * 700; //500;
    var width = 700;
    var height = 3 / 6 * width;
    var fontsize = Math.max(width * 0.05, 16)

    var force = d3.layout.force()
        .charge(-30)
        .linkDistance(100)
        .size([width, height])
        .nodes(mpnet.nodes)
        .links(mpnet.links)
        .start();



    mpnet.layers = mpnet.layers.filter(layer => {
        if (layer.name === 'organization') return isOrgActive;
        if (layer.name === 'location') return isLocActive;
        if (layer.name === 'person') return isPerActive;
    })
    var nlayers = mpnet.layers.length;
    for (var layer = nlayers - 1; layer >= 0; layer--) {
        svg_layer[layer] = d3.select(".svg-body").append("svg")
            .attr("layer", 0)
            .style("position", "absolute")
            .style("left", "100px")
            .style("top", (0 + layer * width / 4.5).toString() + "px")
            .style("background-color", "rgba(100,100,100,0.3)")
            .style("transform", "rotate3D(-0.9,0.4,0.4,70deg)") // Firefox
            .style("-webkit-transform", "rotate3D(-0.9,0.4,0.4,70deg)") // Safari, Chrome
            .attr("width", width)
            .attr("height", height);




        layer_label[layer] = svg_layer[layer].selectAll(".layerlabel")
            .data([mpnet.layers[layer]])
            .enter()
            .append("text")
            .text((d) => d.name)
            .attr("dx", function(d) { return width - 0.8 * d.name.toString().length * fontsize; })
            .attr("dy", fontsize)
            .style("font-size", fontsize + "px")
            .style("fill", "white")

        link_layer[layer] = svg_layer[layer].selectAll(".link")
            .data(mpnet.links)
            .enter()
            .append("line")
            .filter(function(d) {

                if (d.layer == layer && d.layer === d.layer_to) {
                    return d.layer === layer
                }
            })

        .style("stroke-width", function(d) { return 2 * Math.sqrt(d.value); })
            .style("stroke", "#999");

        node_layer[layer] = svg_layer[layer].selectAll(".node")
            .data(mpnet.nodes)
            .enter()
            .append("circle")
            .filter(function(d) { return d.layer === layer })
            .attr("class", "node")
            .attr("r", 10)
            .style("fill", function(d) { return color(d.index); })
            .style("stroke", "#fff")
            .style("stroke-width", "1.5px")
            .call(force.drag);

        node_layer[layer].append("title")
            .text(function(d) { return d.name; });


    }

    var nlinks = mpnet.links.length;
    var count = 0;




    force.on("tick", function() {

        for (var layer = 0; layer < nlayers; layer++) {
            link_layer[layer].attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });


            node_layer[layer].attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; });



        }
    });
}


$(document).ready(function() {

    $("#selectFile").click(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            contentType: "application/json;charset=utf-8",
            url: `${window.origin}/`,
            traditional: "true",
            data: JSON.stringify('selectFile'),
            dataType: "json",
            success: function(response) {}
        });
    });

    $("#filterData").click(function(e) {
        $('#instruct-text').hide();
        d3.select(".svg-body").selectAll("*").remove();
        e.preventDefault();
        $.ajax({
            type: "POST",
            contentType: "application/json;charset=utf-8",
            url: `${window.origin}/`,
            traditional: "true",
            data: JSON.stringify(['date', startDate, endDate]),
            dataType: "json",
            success: function(response) {
                render(response);
            }
        });
    });


    $("#load-button").click(function(e) {
        e.preventDefault();
        location.reload();

    });

    $("#render").click(function(e) {
        $('#instruct-text').hide();
        d3.select(".svg-body").selectAll("*").remove();

        $.ajax({
            type: "POST",
            contentType: "application/json;charset=utf-8",
            url: `${window.origin}/`,
            traditional: "true",
            data: JSON.stringify('render'),
            dataType: "json",
            success: function(response) {
                render(response);

            }




        });
    });
});