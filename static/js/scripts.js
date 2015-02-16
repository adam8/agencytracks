$(function() {

  $( "#container" ).on( "click", ".toggle-next", function(e) {
    e.preventDefault();
    $(this).hide().next('.toggle-this').addClass('toggle-visible').find('input:eq(0)').focus();
  });
  
  $( "#container" ).on( "click", ".trigger-next", function(e) {
    e.preventDefault();
    $(this).next('.toggle-this').slideToggle(100).find('.pure-control-group:eq(0)>:first-child').focus();
    if (e.target.id == "notes-level-toggle") {
      $('.balance-text').balanceText();
    }
  });  
  
  $( "#container" ).on( "click", ".cancel-this", function(e) {
    e.preventDefault();
    $(this).closest('.toggle-this').slideToggle(100);
  });
  
  $( '.step-title-trigger' ).click(function(e) {
    e.preventDefault();
    // Load the tasks for this step
    $(this).siblings('.step-tasks').load( "/clients/" + $(this).data('client') + "/steps/" + $(this).data('step') , function() {
        $(this).slideToggle(100);
    });
  });
  
  $( "#steps" ).on( "change", "input[type='checkbox']", function(e) {
    $(this).parent().find('.time-actual').focus();
    var $input = $(this);
    var client = $(this).data('client');
    var task = $(this).data('task');
    var done;
    if ( $(this).is(':checked') ) {
      done = "True";
    } else {
      done = "False";
    }
    $input.attr('disabled','disabled');
    $.post( "/clients/" + client + "/steps/" + task, {"done": done}).done(function() {
       $input.removeAttr('disabled');
     });
  });
  
  $( "#steps" ).on( "change", ".time-estimate", function(e) {
    var client = $(this).data('client');
    var task = $(this).data('task');
    var time_estimate = $(this).val();
    $.post( "/clients/" + client + "/steps/" + task, {"time_estimate": time_estimate}).done(function() {
       console.log('done!!')
    });
  });
  
  $( "#steps" ).on( "change", ".time-actual", function(e) {
    var client = $(this).data('client');
    var task = $(this).data('task');
    var time_actual = $(this).val();
    if ($(this).val() == "") {
      time_actual = 0;
    }
    var time_estimate = parseInt($(this).siblings('.time-estimate').eq(0).attr("placeholder"));
    if (time_actual > time_estimate) {
      $(this).addClass("time-over-estimate");
    } else {
      $(this).removeClass("time-over-estimate");
    }
    $.post( "/clients/" + client + "/steps/" + task, {"time_actual": time_actual}).done(function() {
      console.log('done, yep');
    });
  });
  
  $( "#steps" ).on( "change", ".task-order", function(e) {
    var client = $(this).data('client');
    var task = $(this).data('task');
    var order = $(this).val();
    $.post( "/clients/" + client + "/steps/" + task, {"order": order}).done(function() {
       console.log('success')
    });
  });
  
  $( "#steps" ).on( "change", ".task-type", function(e) {
    var client = $(this).data('client');
    var task = $(this).data('task');
    var task_type = $(this).val();
    $.post( "/clients/" + client + "/steps/" + task, {"task_type": task_type}).done(function() {
       console.log('success')
    });
  });
  
  $( "#steps" ).on( "blur", ".task-text", function(e) {
    if ( $(this).data('original') != $(this).html() ) {
      //console.log('original: ' + $(this).data('original'))
      //console.log('html: ' + $(this).html())
      var client = $(this).data('client');
      var task = $(this).data('task');
      var task_text = $(this).html();
      $.post( "/clients/" + client + "/steps/" + task, {"task_text": task_text}).done(function() {
         console.log('success')
      });
    }
  });
  
  $( "#steps" ).on( "click", ".task-indent", function(e) {
    var client = $(this).data('client');
    var task = $(this).data('task');
    var $this = $(this);
    $.post( "/clients/" + client + "/steps/" + task, {"indent": "True"}).done(function() {
      console.log('success');
      if ($this.closest('.task-list-item.indent').length) {
        $this.closest('.task-list-item').removeClass('indent');
      $this.html('&#10140;');
      } else {
        $this.closest('.task-list-item').addClass('indent');
      $this.html('&#11013;');
      }
    });
  });
  
  /*
  $( "#questionnaire-form" ).on( "submit", function( e ) {
    e.preventDefault();
    var client = $(this).data("client");
    $.post( "/clients/" + client + "/questionnaire", $(this).serialize() ).done(function(data) {
      //console.log(data);
      if (data=="success") {
        window.location.href = "/clients/" + client;
      }
    });
  });
  */
  
  $( "input[type=url]" ).on( "blur", function( e ) {
    console.log(e.target.value);
    string = e.target.value;
    if( string != "" && !(/^http:\/\//.test(string)) && !(/^https:\/\//.test(string)) ){
        string = "http://" + string;
    }
    e.target.value = string;
  });
  
  // $( "#widget-notes" ).mouseover(function() {
//     var $input = $(this).find('.note-create-form-client-input');
//     if ($input.html() == $input.data('default-message')) {
//       $(this).find('.note-create-form-client-input').empty().focus();
//     }
//   });
  
  $( "#widget-notes" ).on( "click", ".note-create-form-client .note-entry", function(e) {
    $client_input = $(this).find('.note-create-form-client-input');
    if ($client_input.html() == $client_input.data('default-message')) {
      // console.log('clicked');
      $client_input.text("");
      $client_input.removeClass('note-muted');
      $client_input.focus();
    }
  });
  
  $( "#widget-notes" ).keypress(function(e) {
    if (e.which==13) {
      e.preventDefault();
      var msg = $(this).find('.note-create-form-client-input').html();
      if ($(this).html() != $(this).data('default-message') && msg != "") {
        var client = $(this).data('client');
        var user = $(this).data('user');
        $.post( "/clients/" + client + "/notes/" + user, { "note": msg }).done(function(data) {
          //console.log(data);
          $('#widget-notes').load( "/dashboard/" + client + "/notes/" + user , function(data) {
              // if data == "success" hide spinner
            console.log("done", data)
          });
        });
      }
    }
  });
  
  $( "#widget-notes" ).on( "blur", ".note-create-form-client-input", function(e) {
    if ($(this).html() == "") {
      $(this).text( $(this).data('default-message') ); 
      $(this).addClass('note-muted');
    }
  });
  
  // Load client / the level notes
  if ($('#widget-notes').length) {
    var client = $('#widget-notes').data('client');
    var user = $('#widget-notes').data('user');
    $('#widget-notes').load( "/dashboard/" + client + "/notes/" + user , function(data) {
        // if data == "success" hide spinner
      console.log("done")
    });
  }
  
  $('.widget-item').click(function(e) {
    if ( $(this).find('.widget-link').length ) {
      window.location.href = $(this).find('.widget-link:first').attr('href');
    }
  })
  
  // Don't let single word wrap... so last two words are attached by &nbsp;
  /* Using balance-text instead: https://github.com/adobe-webplatform/balance-text
  
  $(".widget-text").each(function() {
    var wordArray = $(this).text().split(" ");
    if (wordArray.length > 3) {
      wordArray[wordArray.length-2] += "&nbsp;" + wordArray[wordArray.length-1];
      wordArray.pop();
      $(this).html(wordArray.join(" "));
    }
  });
  $(".widget-item h2").each(function() {
    var wordArray = $(this).text().split(" ");
    if (wordArray.length > 3) {
      wordArray[wordArray.length-2] += "&nbsp;" + wordArray[wordArray.length-1];
      wordArray.pop();
      $(this).html(wordArray.join(" "));
    }
  });
  */
  
  
});