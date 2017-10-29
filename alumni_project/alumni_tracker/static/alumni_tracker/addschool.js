    var counter = 1;

    //var limit = 3;

    function addInput(divName){

      var newdiv = document.createElement('div');

      newdiv.innerHTML = "School name" + (counter + 1) + "<br><input type='text' name=school_name[]>"  
      + "  School city" + counter + 1 + "<br><input type=text' name='school_city[]'> " 
      + "Programme" + counter +  1 + "<br><input type=text' name='programme[]'> "
      + " Grad year" + counter +  1 + "<br><input type=text' name='grad-year[]'>";

      document.getElementById(divName).appendChild(newdiv);

      counter++;
    }