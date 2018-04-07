function setup() {

    loadJSON('https://newsapi.org/v2/top-headlines?sources=bbc-sport&apiKey=999a69895a874eb5859727b55b516dc6',gotData)
}


function gotData(data) {
println(data)
}