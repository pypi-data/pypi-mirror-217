$('#orpa-mouse-function-select')
    .dropdown()
;

$('#orpa-keyboard-function-select')
    .dropdown()
;

$(document).ready(function() {
    
    var l_result_cv2_bool = orpa_api_activity_list_execute_sync("importlib.util.find_spec",["cv2"])
    if (JSON.parse(l_result_cv2_bool)[0] == null) {
        $('#orpa-screen-accuracy-img-locate').prop('disabled', true);
        $('#orpa-screen-accuracy-img-locate').val('1.0');
    }
        var l_response_data = null
        ///Загрузка локации project
        $.ajax({
            type: "POST",
            url: '/api/orpa-screen-img-tree-location-path',
            success: function(in_data)
              {
                  l_response_data = in_data
              },
            async:false,
        });
        $('#orpa-mouse-screen-dir-location').val(l_response_data)
        orpa_screen_dir_render()
})


orpa_before_action_focus = function(in_selector, in_selector_type, in_wait_time) {
    var l_result_list = ""
    if (in_selector != ""){
        if (in_selector_type == "UIO") {
            in_selector = JSON.parse('['+in_selector+']')
        }
        var l_arg_list = in_selector
        var l_activity_name_str = "pyOpenRPA.Robot.UIDesktop.UIOSelector_FocusHighlight"
        l_result_list = orpa_api_activity_list_execute_sync(l_activity_name_str, l_arg_list, null)
        // Проверка на возможную ошибку (для ShowModal)
        if (l_result_list.includes("ErrorTraceback")==true) {l_result_list=JSON.parse(l_result_list)}
    }
    var l_arg_list_2 = [parseFloat(in_wait_time)]
    orpa_api_activity_list_execute_sync("time.sleep", l_arg_list_2, null)
    return l_result_list
}

//  РАЗДЕЛ КЛАВИАТУРА & БУФЕР -- ORPA-KEYBOARD -- НАЧАЛО 

orpa_keyboard_symbol_encode = function(symbol) {
    if (symbol.includes(" ")) {symbol = symbol.replace(" ","_")}
    if (symbol.includes("-") && symbol.length>1) {symbol = symbol.replace("-","_")}
    for (var key in keys_dict) {
        if (key == symbol.toUpperCase()) {return keys_dict[key]}
      }
    return null
}

orpa_keyboard_do_function = function () {
    //Фокус и ожидание перед выполнение функции
    var l_selector = $('.orpa-before-action-focus-keyboard').val()
    var l_wait_time = $('.ui.tag.label.teal.tiny.noselect.keyboard-wait-time').html().substring(0,3)
    var l_selector_type = $('.ui.tag.label.teal.tiny.noselect.keyboard-selector-type').html()
    var l_result_activity = orpa_before_action_focus(l_selector, l_selector_type, l_wait_time)
    // Либо модальное окно с ошибкой, либо выполнение функции
    if (typeof(l_result_activity)=="object") {
        mGlobal.ShowModal(l_result_activity["ErrorHeader"],l_result_activity["ErrorTraceback"])
    }
    else {
        //Основная функция (Keyboard.Down/Up/Send/Wait)
        var l_activity_name_str = "pyOpenRPA.Robot.Keyboard."+document.getElementsByName('orpa-keyboard-action')[0].value
        var l_KeyInt = $('#orpa-keyboard-function-symbol-select').val()
        l_KeyInt = parseInt(orpa_keyboard_symbol_encode(l_KeyInt))
        var l_arg_dict = {"inKeyInt":l_KeyInt}
        orpa_api_activity_list_execute_sync(l_activity_name_str, null, l_arg_dict)   
    }
}

orpa_keyboard_do_write_function = function() {
    //Фокус и ожидание перед выполнение функции
    var l_selector = $('.orpa-before-action-focus-keyboard').val()
    var l_wait_time = $('.ui.tag.label.teal.tiny.noselect.keyboard-wait-time').html().substring(0,3)
    var l_selector_type = $('.ui.tag.label.teal.tiny.noselect.keyboard-selector-type').html()
    var l_result_activity = orpa_before_action_focus(l_selector, l_selector_type, l_wait_time)
    // Либо модальное окно с ошибкой, либо выполнение функции
    if (typeof(l_result_activity)=="object") {
        mGlobal.ShowModal(l_result_activity["ErrorHeader"],l_result_activity["ErrorTraceback"])
    }
    else {
        //Основная функция (Keyboard.Write)
        var l_activity_name_str = "pyOpenRPA.Robot.Keyboard.Write"
        var l_text = $('.orpa-keyboard-write-data').val()
        var l_arg_dict = {"inTextStr":l_text}
        orpa_api_activity_list_execute_sync(l_activity_name_str, null, l_arg_dict)
    }
}

orpa_keyboard_do_function_hotkey = function() {
    //Фокус и ожидание перед выполнение функции
    var l_selector = $('.orpa-before-action-focus-keyboard').val()
    var l_wait_time = $('.ui.tag.label.teal.tiny.noselect.keyboard-wait-time').html().substring(0,3)
    var l_selector_type = $('.ui.tag.label.teal.tiny.noselect.keyboard-selector-type').html()
    var l_result_activity = orpa_before_action_focus(l_selector, l_selector_type, l_wait_time)
    // Либо модальное окно с ошибкой, либо выполнение функции
    if (typeof(l_result_activity)=="object") {
        mGlobal.ShowModal(l_result_activity["ErrorHeader"],l_result_activity["ErrorTraceback"])
    }
    else {
        //Основная функция (Keyboard.HotkeyCombination)
        var l_activity_name_str = "pyOpenRPA.Robot.Keyboard.HotkeyCombination"
        var l_special_symbol_list = document.getElementsByClassName('ui tag label teal tiny noselect keyboard-hotkey')
        var l_special_symbol_str = ""
        var l_arg_list = []
        for (var j=0;j<l_special_symbol_list.length; j++) {
                l_special_symbol_str = l_special_symbol_list[j].innerHTML
                var l_special_symbol_int = 0
                if (l_special_symbol_str == "ctrl") {l_special_symbol_int=0x1D} 
                else if (l_special_symbol_str == "alt") {l_special_symbol_int=0x38} 
                else if (l_special_symbol_str == "shift") {l_special_symbol_int=0x2A} 
                else if (l_special_symbol_str == "win") {l_special_symbol_int=57435}
                l_arg_list.push(l_special_symbol_int)
            }
        var l_common_symbol_int = $('#orpa-keyboard-hotkey-common-symbol-select').val()
        l_common_symbol_int = parseInt(orpa_keyboard_symbol_encode(l_common_symbol_int))
        l_arg_list.push(l_common_symbol_int)
        orpa_api_activity_list_execute_async(null, l_activity_name_str, l_arg_list, null)
    }
}
 
orpa_keyboard_clipboard_get = function() {
    var l_activity_name_str = "pyOpenRPA.Robot.Clipboard.Get"
    var l_result = orpa_api_activity_list_execute_sync(l_activity_name_str, null, null)
    $('#orpa-keyboard-clipboard-textarea').val(l_result.slice(0,-1).substring(1))
}

orpa_keyboard_clipboard_set = function() {
    var l_activity_name_str = "pyOpenRPA.Robot.Clipboard.Set"
    var l_text_area_str = $('#orpa-keyboard-clipboard-textarea').val()
    var l_arg_list = [l_text_area_str]
    orpa_api_activity_list_execute_sync(l_activity_name_str, l_arg_list, null)
}

//  РАЗДЕЛ КЛАВИАТУРА & БУФЕР -- ORPA-KEYBOARD -- КОНЕЦ 

//  РАЗДЕЛ МЫШЬ & ЭКРАН -- ORPA-MOUSE -- НАЧАЛО 

// Функция по отрисовке дерева файлов внутри "Локации"
orpa_screen_dir_render = function() {
    var l_path = $('#orpa-mouse-screen-dir-location').val()
    var l_data_dict = {
        "Path": l_path,
      }
    var l_response_data=null
    ///Загрузка данных
    $.ajax({
      type: "POST",
      url: '/api/orpa-screen-img-tree',
      data: JSON.stringify(l_data_dict),
      success: function(in_data)
        {
            l_response_data = JSON.parse(in_data)
        },
      dataType: "text",
      async:false,
    });
    var l_img_tree = $('.ui.list.img.tree')
    l_img_tree.css({"backgroundColor":"white"})
    var l_html_str = ''
    // Если пришла строка - то ошибка в поиске директории
    if ("ErrorTraceback" in l_response_data == true) {
        mGlobal.ShowModal(l_response_data["ErrorHeader"], l_response_data["ErrorTraceback"])
    }
    // Иначе - отрисовываем содержимое (только файлы)
    else {
        for (var j=0;j<l_response_data.length; j++) {
            l_html_str += `<div class="orpa-screen-img-dir-item-conteiner">
            <div class="img-tree-item-${j}" onclick="orpa_api_snipingtool_screenshot_render($('.img-tree-item-${j}'))">${l_response_data[j]}</div>
            <span class="orpa-screen-img-tree-item-action" onclick="orpa_api_img_tree_item_detect($('.img-tree-item-${j}'))">Распознать</span>&emsp;
            <span class="orpa-screen-img-tree-item-action" onclick="orpa_mouse_image_do_function($('.img-tree-item-${j}'))">Найти</span>&emsp;
            <span class="orpa-screen-img-tree-item-action" onclick="orpa_api_img_tree_item_rename($('.img-tree-item-${j}'))">Переименовать</span>&emsp;
            <span class="orpa-screen-img-tree-item-action" onclick="orpa_api_img_tree_item_delete($('.img-tree-item-${j}'))">Удалить</span></div>`
        } 
    }
    l_img_tree.html(l_html_str)
    var l_date = new Date()
    $('#orpa-mouse-screen-save-location').val(`${l_date.getFullYear()}_${l_date.getMonth()}_${l_date.getDate()}.png`)
}

// Инициация snipingtool (ножницы)
orpa_screen_sniping_tool = function() {
    var l_activity_name_str = "pyOpenRPA.Robot.Screen.InitSnipingTool"
    var l_path = $('#orpa-mouse-screen-dir-location').val() + "\\" + $('#orpa-mouse-screen-save-location').val()
    //Фокус и ожидание перед выполнение функции
    var l_selector = $('.orpa-before-action-focus-screen').val()
    var l_wait_time = $('.ui.tag.label.teal.tiny.noselect.screen-wait-time').html().substring(0,3)
    var l_selector_type = $('.ui.tag.label.teal.tiny.noselect.screen-selector-type').html()
    var l_result_activity = orpa_before_action_focus(l_selector, l_selector_type, l_wait_time)
    //SnipingTool - отработка
    if (typeof(l_result_activity)=="object") {
        mGlobal.ShowModal(l_result_activity["ErrorHeader"],l_result_activity["ErrorTraceback"])
    }
    else {
        var l_arg_dict = {"inPath":l_path}
        orpa_api_activity_list_execute_sync(l_activity_name_str, null, l_arg_dict)
        orpa_screen_dir_render()
        if (l_selector!="") {orpa_api_activity_list_execute_async(null, "pyOpenRPA.Robot.Keyboard.HotkeyCombination", [0x38,0x0F], null)}
    }
}

// Реализация предпросмотра
orpa_api_snipingtool_screenshot_render = function (in_filename) {
    var l_path = $('#orpa-mouse-screen-dir-location').val() + "\\" + in_filename.html()
    var l_data_dict = {
      "Path": l_path,
    }
    var l_response_data=null
    ///Загрузка данных
    $.ajax({
      type: "POST",
      url: '/api/snipingtool-screenshot-render',
      data: JSON.stringify(l_data_dict),
      success: function()
        {
            var l_rnd = Math.floor(Math.random() * 100)
            if ($('#orpa-mouse-screen-img').length==0) {
                var img = "<img id='orpa-mouse-screen-img' src='http://127.0.0.1:8081/api/snipingtool-screenshot-render' style='height:225px;width:100%;object-fit:contain;'>";
                $('.orpa-placeholder-img-preview').html(img);
                $('#orpa-screen-render-filename').html(`ПРЕДПРОСМОТР - ${in_filename.html()}`)
            }
            else {
                $('#orpa-mouse-screen-img').attr("src",`http://127.0.0.1:8081/api/snipingtool-screenshot-render?${l_rnd}`)
                $('#orpa-screen-render-filename').html(`ПРЕДПРОСМОТР - ${in_filename.html()}`)
            }
        },
      dataType: "text",
      async:false,
    });
    return l_response_data
}

// Распознование текста на картинке
orpa_api_img_tree_item_detect = function(in_filename){
    var l_path = $('#orpa-mouse-screen-dir-location').val() + "\\" + in_filename.html()
    $('#orpa-screen-teseract-location').val(l_path)
}

// Удаление файлов из img tree
orpa_api_img_tree_item_delete = function(in_filename){
    var l_path = $('#orpa-mouse-screen-dir-location').val() + "\\" + in_filename.html()
    var l_data_dict = {
      "Path": l_path,
    }
    var l_response_data=null
    ///Загрузка данных
    $.ajax({
      type: "POST",
      url: '/api/orpa-screen-img-tree-item-delete',
      data: JSON.stringify(l_data_dict),
      success: function(in_data)
        {
            l_response_data = JSON.parse(in_data)
        },
      dataType: "text",
      async:false,
    });
    if ( l_response_data==null ) {
        orpa_screen_dir_render()
    }
    // Если пришла строка - то ошибка в поиске директории
    else if ("ErrorTraceback" in l_response_data == true) {
        mGlobal.ShowModal(l_response_data["ErrorHeader"],l_response_data["ErrorTraceback"])
    }
}

// Нахождение картинки из img tree
orpa_mouse_image_do_function = function(in_filename) {
    var l_activity_name_str  = "pyOpenRPA.Robot.Screen.ImageLocateAllInfo"
    var l_path = $('#orpa-mouse-screen-dir-location').val() + "\\" + in_filename.html()
    //Фокус и ожидание перед выполнение функции
    var l_selector = $('.orpa-before-action-focus-screen').val()
    var l_wait_time = $('.ui.tag.label.teal.tiny.noselect.screen-wait-time').html().substring(0,3)
    var l_selector_type = $('.ui.tag.label.teal.tiny.noselect.screen-selector-type').html()
    var l_result_activity = orpa_before_action_focus(l_selector, l_selector_type, l_wait_time)
    // ImageLocateAll - отработка
    if (typeof(l_result_activity)=="object") {
        mGlobal.ShowModal(l_result_activity["ErrorHeader"],l_result_activity["ErrorTraceback"])
    }
    else{
        // Учет точности, если установлен cv2
        if ($('#orpa-screen-accuracy-img-locate').is(':disabled') == true) {
            var l_arg_dict = {"inImgPathStr":l_path}
        }
        else {
            var l_confidence_float = parseFloat($('#orpa-screen-accuracy-img-locate').val())
            var l_arg_dict = {"inImgPathStr":l_path, "inConfidenceFloat":l_confidence_float}
        }
        // Получение результата
        var l_result_str = orpa_api_activity_list_execute_sync(l_activity_name_str, null, l_arg_dict)
        var l_result = JSON.parse(l_result_str)
       
        // Отрисовка результата
        var l_html_str = ""
        var l_sut_str = $('#orpa-screen-sut-img-locate').val()

        if (l_sut_str.length != 2) {mGlobal.ShowModal("Неверно задано символьное указание точки (СУТ)","")}
        else {
            if (l_result.length>0) {
                $(".orpa-placeholder-locate-result").css({"backgroundColor":"white"})
            }
            for (var j=0;j<l_result.length; j++) {
                l_render_data = l_result[j]
                /*if (l_render_data.includes(null)) {
                    mGlobal.ShowModal("Неверно задано символьное указание точки (СУТ)","")
                    break
                }*/
                l_html_str += `<div class="orpa-screen-locate-result-conteiner" onclick="orpa_screen_location_args_fill($('.orpa-screen-locate-result-coord-x-${j}').attr('value'),$('.orpa-screen-locate-result-coord-y-${j}').attr('value'))">
                <div class="orpa-screen-locate-result-${j}" style="font-size: 14px"><b>Область ${j}</b></div>
                <span class="orpa-screen-locate-result-coord-x-${j}" value="${l_render_data.left}" style="font-size: 12px">X: ${l_render_data.left}</span>&emsp;
                <span class="orpa-screen-locate-result-coord-y-${j}" value="${l_render_data.top}" style="font-size: 12px">Y: ${l_render_data.top}</span>&emsp;
                <span class="orpa-screen-locate-result-coord-w-${j}" value="${l_render_data.width}" style="font-size: 12px">W: ${l_render_data.width}</span>&emsp;
                <span class="orpa-screen-locate-result-coord-h-${j}" value="${l_render_data.height}" style="font-size: 12px">H: ${l_render_data.height}</span>&emsp;</div>`
            }
        }
        $(".orpa-placeholder-locate-result").html(l_html_str)
        if (l_selector!="") {orpa_api_activity_list_execute_async(null, "pyOpenRPA.Robot.Keyboard.HotkeyCombination", [0x38,0x0F], null)}
    }  
}

// Переименовка из img tree
orpa_api_img_tree_item_rename = function(in_filename) {
    var l_path = $('#orpa-mouse-screen-dir-location').val() + "\\" + in_filename.html()
    var l_new_filename = prompt("Введите новое имя файла", '')
    if (l_new_filename==null) {l_new_filename=in_filename.html()}
    var l_new_path = $('#orpa-mouse-screen-dir-location').val() + "\\" + l_new_filename
    var l_data_dict = {
        "Path": l_path,
        "NewPath": l_new_path
      }
    var l_response_data=null
    ///Загрузка данных
    $.ajax({
      type: "POST",
      url: '/api/orpa-screen-img-tree-item-rename',
      data: JSON.stringify(l_data_dict),
      success: function(in_data)
        {
            l_response_data = JSON.parse(in_data)
        },
      dataType: "text",
      async:false,
    });
    if ( l_response_data==null ) {
        orpa_screen_dir_render()
    }
    else if ("ErrorTraceback" in l_response_data == true) {
        mGlobal.ShowModal(l_response_data["ErrorHeader"],l_response_data["ErrorTraceback"])
    }
}

// Вывод результатов LocateAll
orpa_screen_location_args_fill = function(x,y) {
    var l_arg_list = `[${x},${y}]`
    $('#mouse-argument-dataset').val(l_arg_list)
}

// Инициация функций модуля Mouse
orpa_mouse_do_function = function() {
    //Фокус и ожидание перед выполнение функции
    var l_selector = $('.orpa-before-action-focus-screen').val()
    var l_wait_time = $('.ui.tag.label.teal.tiny.noselect.screen-wait-time').html().substring(0,3)
    var l_selector_type = $('.ui.tag.label.teal.tiny.noselect.screen-selector-type').html()
    var l_result_activity = orpa_before_action_focus(l_selector, l_selector_type, l_wait_time)
    // Mouse function
    if (typeof(l_result_activity)=="object") {
        mGlobal.ShowModal(l_result_activity["ErrorHeader"],l_result_activity["ErrorTraceback"])
    }
    else {
        var l_activity_name_str = "pyOpenRPA.Robot.Mouse."+document.getElementsByName('orpa-mouse-action')[0].value
        var l_arg_type_list = $('.ui.tag.label.teal.tiny.noselect.mouse-arg-type')
        var l_arg_type_str = ""
        if (l_arg_type_list.html() == "СПИСОК") {l_arg_type_str = "list"}
        else {l_arg_type_str = "dict"}
    
        if (l_arg_type_str == "list") {
            var l_arg_list = $('#mouse-argument-dataset').val().replace("[","").replace("]","").split(",")
            for (var j=0;j<l_arg_list.length; j++) {
                l_arg_list[j] = parseInt(l_arg_list[j])
            } 
            orpa_api_activity_list_execute_async(null,l_activity_name_str, l_arg_list, null)
        }
        else if (l_arg_type_str == "dict") {
            var l_arg_dict = JSON.parse($('#mouse-argument-dataset').val())
            orpa_api_activity_list_execute_async(null,l_activity_name_str, null, l_arg_dict)
        }
    }
}

// Реализация просмотра tesseract
orpa_api_tesseract_render = function () {
    var l_path = $('#orpa-screen-teseract-location').val()
    var l_data_dict = {
      "Path": l_path,
    }
    var l_response_data=null
    ///Загрузка данных
    $.ajax({
      type: "POST",
      url: '/api/orpa-screen-tesseract-run',
      data: JSON.stringify(l_data_dict),
      success: function(in_data)
        {
            l_response_data = JSON.parse(in_data)
        },
      dataType: "text",
      async:false,
    });
    if ("ErrorTraceback" in l_response_data == true) {
        mGlobal.ShowModal(l_response_data["ErrorHeader"],l_response_data["ErrorTraceback"])
    }
    else {
        var l_html_str = `<div class="orpa-screen-tesseract-result">${l_response_data[0]}</div>`
        $('.orpa-placeholder-tesseract-result').css({"backgroundColor":"white"});
        $('.orpa-placeholder-tesseract-result').html(l_html_str);
    }

}

// Парсер символьного указания точки
orpa_sut_parse = function(in_sut_str, in_box_list) {
    var l_x_int = null
    var l_y_int = null
    // Вычисление координаты x
    if (in_sut_str[0].toUpperCase() == "C") {l_x_int = parseInt(in_box_list['left']) + parseInt(parseInt(in_box_list['width'])/2)}
    else if (in_sut_str[0].toUpperCase() == "L") {l_x_int = parseInt(in_box_list['left'])}
    else if (in_sut_str[0].toUpperCase() == "R") {l_x_int = parseInt(in_box_list['left']) + parseInt(in_box_list['width'])}
    // Вычисление координаты y
    if (in_sut_str[1].toUpperCase() == "C") {l_y_int = parseInt(in_box_list['top']) + parseInt(parseInt(in_box_list['height'])/2)}
    else if (in_sut_str[1].toUpperCase() == "U") {l_y_int = parseInt(in_box_list['top'])}
    else if (in_sut_str[1].toUpperCase() == "D") {l_y_int = parseInt(in_box_list['top']) + parseInt(in_box_list['height'])}
    return [l_x_int, l_y_int]
}


orpa_mouse_workspace_proportion_set = function (in_col_1, in_col_2, in_col_3) {
    l_class_list = ["one","two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "elewen", "twelve", "thirdteen", "fourteen", "fifthteen", "sixteen"]
    l_object_list = [$("#orpa-mouse-col-1")[0], $("#orpa-mouse-col-2")[0], $("#orpa-mouse-col-3")[0]] 
    l_object_col_list =[in_col_1, in_col_2, in_col_3]
    for (var j=0;j<l_object_list.length; j++) {
      for (var i=0;i<l_class_list.length; i++) {
        l_class = l_class_list[i]
        
        if (l_object_list[j].classList.contains(l_class)) {
          l_object_list[j].classList.remove(l_class)
          l_object_list[j].classList.remove("wide")
          l_object_list[j].classList.remove("column")
        }
      }
      l_object_list[j].classList.add(l_object_col_list[j])
      l_object_list[j].classList.add("wide")
      l_object_list[j].classList.add("column")
    }
  }

  //  РАЗДЕЛ МЫШЬ & ЭКРАН -- ORPA-MOUSE -- КОНЕЦ 
  
//   !!! Функции по копированию кода !!!
// Копирование функций блока СИМВОЛ
orpa_keyboard_do_function_copy = function() {
    var l_activity_name_str = "pyOpenRPA.Robot.Clipboard.Set"
    var l_func_name_str = document.getElementsByName('orpa-keyboard-action')[0].value
    if (l_func_name_str == "") {l_func_name_str="Send"}
    var l_KeyInt = $('#orpa-keyboard-function-symbol-select').val()
    if (l_KeyInt == "") {l_KeyInt = "Keyboard.KEY_ENG_A"}
    else {l_KeyInt = parseInt(orpa_keyboard_symbol_encode(l_KeyInt))}
    var l_text_area_str = `from pyOpenRPA.Robot import Keyboard\nKeyboard.${l_func_name_str}(${l_KeyInt})`
    var l_arg_list = [l_text_area_str]
    orpa_api_activity_list_execute_sync(l_activity_name_str, l_arg_list, null)
}

// Копирование функций блока ГОРЯЧИЕ КЛАВИШИ
orpa_keyboard_do_function_hotkey_copy = function() {
    var l_activity_name_str = "pyOpenRPA.Robot.Clipboard.Set"
    var l_func_name_str = "HotkeyCombination"
    var l_special_symbol_list = document.getElementsByClassName('ui tag label teal tiny noselect keyboard-hotkey')
    var l_special_symbol_final_str = ""
    for (var j=0;j<l_special_symbol_list.length; j++) {
            var l_special_symbol_str = l_special_symbol_list[j].innerHTML
            var l_special_symbol_int = 0
            if (l_special_symbol_str == "ctrl") {l_special_symbol_int=0x1D} 
            else if (l_special_symbol_str == "alt") {l_special_symbol_int=0x38} 
            else if (l_special_symbol_str == "shift") {l_special_symbol_int=0x2A} 
            else if (l_special_symbol_str == "win") {l_special_symbol_int=57435}
            l_special_symbol_final_str += `${l_special_symbol_int},`
        }
    var l_common_symbol_int = $('#orpa-keyboard-hotkey-common-symbol-select').val()
    if (l_special_symbol_final_str == "" | l_common_symbol_int == "") {
        l_special_symbol_final_str = "Keyboard.KEY_HOT_CTRL_LEFT,"
        l_common_symbol_int = "Keyboard.KEY_ENG_A"
    }
    else{l_common_symbol_int = parseInt(orpa_keyboard_symbol_encode(l_common_symbol_int))}
    var l_text_area_str = `from pyOpenRPA.Robot import Keyboard\nKeyboard.${l_func_name_str}(${l_special_symbol_final_str}${l_common_symbol_int})`
    var l_arg_list = [l_text_area_str]
    orpa_api_activity_list_execute_sync(l_activity_name_str, l_arg_list, null)
}

// Копирование функций блока ТЕКСТ
orpa_keyboard_do_write_function_copy = function() {
    var l_activity_name_str = "pyOpenRPA.Robot.Clipboard.Set"
    var l_func_name_str = "Write"
    var l_text = $('.orpa-keyboard-write-data').val()
    if (l_text == "") {l_text = "Hello World!"}
    var l_text_area_str = `from pyOpenRPA.Robot import Keyboard\nKeyboard.${l_func_name_str}('${l_text}')`
    var l_arg_list = [l_text_area_str]
    orpa_api_activity_list_execute_sync(l_activity_name_str, l_arg_list, null)
}

// Копирование функции Clipboard.Get
orpa_keyboard_clipboard_get_copy = function() {
    var l_activity_name_str = "pyOpenRPA.Robot.Clipboard.Set"
    var l_func_name_str = "Get"
    var l_text_area_str = `from pyOpenRPA.Robot import Clipboard\nlClipStr = Clipboard.${l_func_name_str}()`
    var l_arg_list = [l_text_area_str]
    orpa_api_activity_list_execute_sync(l_activity_name_str, l_arg_list, null)
}

// Копирование функции Clipboard.Set
orpa_keyboard_clipboard_set_copy = function() {
    var l_activity_name_str = "pyOpenRPA.Robot.Clipboard.Set"
    var l_func_name_str = "Set"
    var l_copy_body_str = $('#orpa-keyboard-clipboard-textarea').val()
    if (l_copy_body_str == ""){l_copy_body_str="Hello World!"}
    var l_text_area_str = `from pyOpenRPA.Robot import Clipboard\nlClipStr = Clipboard.${l_func_name_str}('${l_copy_body_str}')`
    var l_arg_list = [l_text_area_str]
    orpa_api_activity_list_execute_sync(l_activity_name_str, l_arg_list, null)
}

// Копирование функции InitSnipingTool
orpa_screen_sniping_tool_copy = function() {
    var l_activity_name_str = "pyOpenRPA.Robot.Clipboard.Set"
    var l_func_name_str = "InitSnipingTool"
    var l_path = $('#orpa-mouse-screen-dir-location').val().replaceAll("\\","\\\\") + "\\\\" + $('#orpa-mouse-screen-save-location').val().replaceAll("\\","\\\\")
    var l_text_area_str = `from pyOpenRPA.Robot import Screen\nScreen.${l_func_name_str}('${l_path}')`
    var l_arg_list = [l_text_area_str]
    orpa_api_activity_list_execute_sync(l_activity_name_str, l_arg_list, null)
}

// Копирование функций модуля Mouse
orpa_mouse_do_function_copy = function() {
    var l_activity_name_str = "pyOpenRPA.Robot.Clipboard.Set"
    var l_func_name_str = document.getElementsByName('orpa-mouse-action')[0].value
    if (l_func_name_str == "") {l_func_name_str="MoveTo"}
    var l_arg_type_list = $('.ui.tag.label.teal.tiny.noselect.mouse-arg-type')
    var l_arg_type_str = ""
    if (l_arg_type_list.html() == "СПИСОК") {l_arg_type_str = "list"}
    else {l_arg_type_str = "dict"}
    if (l_arg_type_str == "list") {
        var l_tmp_arg_list = $('#mouse-argument-dataset').val().replace("[","").replace("]","")
        if (l_tmp_arg_list == "") {
            if (l_func_name_str == "ScrollHorizontal" | l_func_name_str == "ScrollVertical") {l_tmp_arg_list = "250"}
            else {l_tmp_arg_list = "100,100"}
        }
        l_tmp_arg_list = l_tmp_arg_list.split(",")
        for (var j=0;j<l_tmp_arg_list.length; j++) {
            l_tmp_arg_list[j] = parseInt(l_tmp_arg_list[j])
        } 
        var l_text_area_str = `from pyOpenRPA.Robot import Mouse\nMouse.${l_func_name_str}(${l_tmp_arg_list})`
    }
    else if (l_arg_type_str == "dict") {
        var l_tmp_arg_str = $('#mouse-argument-dataset').val().replace(/[{}"]/g, '').replace(/:/g, '=').replace(/,/g, ', ')
        if (l_tmp_arg_str == "") {
            if (l_func_name_str == "ScrollHorizontal" | l_func_name_str == "ScrollVertical") {l_tmp_arg_str = "inScrollClickCountInt=250"}
            else {l_tmp_arg_str = "inXInt=100, inYInt=100"}
        }
        var l_text_area_str = `from pyOpenRPA.Robot import Mouse\nMouse.${l_func_name_str}(${l_tmp_arg_str})`
    }
    var l_arg_list = [l_text_area_str]
    orpa_api_activity_list_execute_sync(l_activity_name_str, l_arg_list, null)
}


var keys_dict = {
    "A": 0x1E,
    "B": 0x30, 
    "C": 0x2E,
    "D": 0x20, 
    "E": 0x12, 
    "F": 0x21,
    "G": 0x22, 
    "H": 0x23, 
    "I": 0x17, 
    "J": 0x24, 
    "K": 0x25, 
    "L": 0x26, 
    "M": 0x32, 
    "N": 0x31, 
    "O": 0x18, 
    "P": 0x19,
    "Q": 0x10, 
    "R": 0x13, 
    "S": 0x1F, 
    "T": 0x14, 
    "U": 0x16,
    "V": 0x2F, 
    "W": 0x11, 
    "X": 0x2D, 
    "Y": 0x15, 
    "Z": 0x2C,
    "Ф": 0x1E, 
    "И": 0x30, 
    "С": 0x2E, 
    "В": 0x20,
    "У": 0x12, 
    "А": 0x21,
    "П": 0x22,
    "Р": 0x23,
    "Ш": 0x17, 
    "О": 0x24,
    "Л": 0x25, 
    "Д": 0x26, 
    "Ь": 0x32,
    "Т": 0x31, 
    "Щ": 0x18, 
    "З": 0x19,
    "Й": 0x10, 
    "К": 0x13, 
    "Ы": 0x1F, 
    "Е": 0x14, 
    "Г": 0x16, 
    "М": 0x2F,
    "Ц": 0x11,
    "Ч": 0x2D, 
    "Н": 0x15, 
    "Я": 0x2C, 
    "Ё": 0x29, 
    "Ж": 0x27, 
    "Б": 0x33, 
    "Ю": 0x34, 
    "Х": 0x1A, 
    "Ъ": 0x1B, 
    "Э": 0x28,
    "F1": 0x3B,
    "F2": 0x3C,
    "F3": 0x3D,
    "F4": 0x3E,
    "F5": 0x3F,
    "F6": 0x40,
    "F7": 0x41,
    "F8": 0x42,
    "F9": 0x43,
    "F10": 0x44,
    "F11": 0x57,
    "F12": 0x58,
    "0": 0xB,
    "1": 0x2,
    "2": 0x3,
    "3": 0x4,
    "4": 0x5,
    "5": 0x6,
    "6": 0x7,
    "7": 0x8,
    "8": 0x9,
    "9": 0xA,
    "~": 0x29,
    ":": 0x27,
    "+": 0x0D,
    "-": 0x0C,
    "<": 0x33,
    ",": 0x33,
    ">": 0x34,
    ".": 0x34,
    "/": 0x35,
    "?": 0x35,
    "[": 0x1A,
    "]": 0x1B,
    "'": 0x28, 
    '"': 0x28,
    "|": 0x2B,
    "\\": 0x2B,
    "ESC": 0x1,
    "BACKSPACE": 0x0E,
    "TAB": 0x0F,
    "ENTER": 0x1C,
    "SHIFT": 0x2A,
    "CTRL": 0x1D,
    "ALT": 0x38,
    "WIN": 57435,
    "CAPS_LOCK": 0x3A,
    "NUM_LOCK": 0x45,
    "END": 0x4F,
    "HOME": 0x47,
    "SPACE": 0x39,
    "PAGE_UP": 0x49,
    "PAGE_DOWN": 0x51,
    "LEFT": 0x4B,
    "UP": 0x48,
    "RIGHT": 0x4D,
    "DOWN": 0x50,
    "PRINT_SCREEN": 0x137,
    "INSERT": 0x52,
    "DELETE": 0x53
}