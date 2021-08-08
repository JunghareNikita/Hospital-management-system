function sidebar_toggle(){
    let sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('hide');
    let main = document.querySelector('.main-content');
    main.classList.toggle('main');
}
function print_function(){
    var div = document.getElementById('invoice');
    var winPrint = window.open('', '', 'left=0, top=0, width=900, height=900, toolbal=0, scrollbars=0, status=0');
    winPrint.document.write('<link rel="stylesheet" href="static/style.css">')
//    winPrint.document.write('<link rel="stylesheet" href="static/bootstrap-4/bootstrap.min.css">')
    winPrint.document.write(div.innerHTML);
    winPrint.document.close();
    winPrint.focus();
    winPrint.print();
    winPrint.close();
}

