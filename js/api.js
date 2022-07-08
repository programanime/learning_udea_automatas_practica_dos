window.api={};
window.api_path=window.location.origin.replace("5555", "5556");

function httpGetAsync(theUrl, callback, headers) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            callback(xmlHttp.responseText);
        }
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    if(headers){
        var keys = Object.keys(headers);
        for(var i=0;i<keys.length;i++){
            var key = keys[i];
            xmlHttp.setRequestHeader(key, headers[key]);
        }
    }else{
        xmlHttp.setRequestHeader('Content-Type', 'text/plain;charset=utf-8');
    }
    xmlHttp.send(null);
}

function httpPostAsync(theUrl, datos, callback, headers) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            callback(xmlHttp.responseText);
        }
    };

    xmlHttp.open("POST", theUrl, true); // true for asynchronous 
    if(headers){
        var keys = Object.keys(headers);
        for(var i=0;i<keys.length;i++){
            var key = keys[i];
            xmlHttp.setRequestHeader(key, headers[key]);
        }
    }
    xmlHttp.send(JSON.stringify(datos));
}


api.get=function(path, callback){
    callback=callback || console.log;
    fetch(window.api_path+path,{
        method: 'GET',
        headers: {'Content-Type': 'application/json'}
    }).then(response => response.json()).then(data => callback(data));    
}

api.post=function(path, body, callback){
    callback=callback || console.log;
    httpPostAsync(window.api_path+path,body,callback);
}
