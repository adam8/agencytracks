if (!RedactorPlugins) var RedactorPlugins = {};

RedactorPlugins.youtube = function() {

  return {
    getTemplate: function() {
          return String()
          + '<section id="redactor-modal-advanced">'
          + '<label>Enter Youtube Link here</label>'
          + '<textarea id="youtube-url" rows="6"></textarea>'
          + '</section>';
      },
      init: function () {
          var button = this.button.add('youtube', 'YouTube');
          this.button.addCallback(button, this.youtube.show);

          // make your added button as Font Awesome's icon
          this.button.setAwesome('youtube', 'fa-youtube');
      },
      show: function() {
          this.modal.addTemplate('youtube', this.youtube.getTemplate());
          this.modal.load('youtube', 'Embed Youtube Video', 400);
          this.modal.createCancelButton();
          var button = this.modal.createActionButton('Insert');
          button.on('click', this.youtube.insert);
          this.selection.save();
          this.modal.show();
          $('#youtube-url').focus();
      },
      insert: function() {
          // var html = $('#mymodal-textarea').val();
          var url = $('#youtube-url').val().trim();
          var html = "";
          if (url.length) {
            // parse out youtube video ID
            var video_id = url.split('v=')[1];
            if (video_id === undefined) {
              video_id = url.split('youtu.be/')[1];
              if (video_id === undefined) {
                if( url.indexOf('iframe') >= 0){
                  var hatchet = url.split('embed/')[1];
                  video_id = hatchet.split('"')[0];
                  if (video_id === undefined) {
                    video_id = url;
                  }
                } else {
                  video_id = url;
                }
              }
            }
            
            html = '<div class="videoWrapper"><iframe width="560" height="315" src="//www.youtube.com/embed/'+ video_id + '" frameborder="0" allowfullscreen></iframe></div>';
          
          }
          this.modal.close();
          this.selection.restore();
          this.insert.html(html);
          this.code.sync();
      }
  };
  
}


