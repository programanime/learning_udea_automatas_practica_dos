window.editor=null;
window.onload = function(){
    window.editor = ace.edit("editor");
    window.editor.setTheme("ace/theme/monokai");
    window.editor.session.setMode("ace/mode/javascript");
    window.editor.setValue(`var a=10;
let b=40;
let c=((a)+(a+b));
const d=20*30;
asdfasdf a=b;
c=(8*10)+30;
var nombre="francisco";
var apellido="javier pacho ";
let nacionalidad = 'colombia';
var n=-10.5e+10;`,1);
}


function compile(){
    var d={"code":window.editor.getValue()};
    api.post("", d, function(response){
        response=JSON.parse(response);
        show_log(response.errores);
        show_lists(response.listas_ligadas);
    });
}

function show_log(errors){
    var log=$("#log");
    log.empty();
    var strHtml=`<div style="color:white;">LOG</div>`;
    var keys = Object.keys(errors);
    var contador=0;
    for(var i=0;i<keys.length;i++){
        var error=errors[keys[i]];
        for(var j=0;j<error.length;j++){
            var e=error[j];        
            strHtml+=`<div><span style="font-weight:bold;">linea ${keys[i]}</span>:<span>${e}</span></div>`;
            contador+=1;
        }
    }
    log.append(strHtml);
    // if(!contador)alert("No se encontraron errores");
}

function show_lists(lists){
    var cola=$("#cola");
    cola.empty();
    var strHtml=`<div style="color:white;">Listas ligadas</div>`;
    var keys = Object.keys(lists);
    
    for(var i=0;i<keys.length;i++){
        var list=lists[keys[i]];
        strHtml+=`<h5 style="text-align:center;margin:0px;">Linea ${keys[i]}</h5>`;
        strHtml+=`<div style="width:100%;border-bottom:2px solid white;padding:1em;">`;
        var temp=[];
        for(var k=0;k<list.length;k++){
            var valor=list[k][1];
            if(valor.trim().length==1 || /^[a-zA-Z0-9]+$/g.test(valor)){
                temp.push(list[k]);
            }else{
                var recorte=0;
                var l=0
                for(l=0;l<valor.length;l++){
                    var c=valor[l];
                    if(["+","-","/","*","%","^","&","|","<",">","{","}","(", ")", "'", '"', "!", "="].indexOf(c)!=-1){
                        if(l>0 && valor.substring(recorte, l))temp.push(["valor", valor.substring(recorte, l)]);
                        temp.push(["simbolo", c]);
                        recorte=l+1;
                    }
                }
                if(l<recorte)temp.push(["valor", valor.substring(recorte, l)]);
            }
        }
        list=temp;
        for(var j=0;j<list.length;j++){
            var nodo=list[j];
            // var e=error[j];
            strHtml+=`<div style="display:inline-block;margin-top:1em;">`;
            strHtml+=`
            <div style="">
                <div style="display:inline-block;background-color:white;">
                    <div style="display:inline-block;padding:0.5em;background-color:#4cacbf;color:white;margin:0px;">${nodo[0]}</div>
                    <div style="display:inline-block;padding:0.5em;background-color:#6cccdf;color:white;">${nodo[1]}</div>
                </div>
            `;
            if(j==list.length-1){
                strHtml+=`<div style="display:inline-block;margin-left: -4px !important;vertical-align: middle;background-color:#333;"><img width="30" src="img/final.png" /></div>`;
            }else{
                strHtml+=`<div style="display:inline-block;margin-left: -4px !important;vertical-align: middle;background-color:#333;"><img width="30" src="img/flecha.png" /></div>`;
            }
            strHtml+=`</div></div>`;
        }
        strHtml+=`</div>`;
    }
    cola.append(strHtml);
}
