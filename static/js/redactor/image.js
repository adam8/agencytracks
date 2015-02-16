if (!RedactorPlugins) var RedactorPlugins = {};

RedactorPlugins.imageUpload = function() {

  return {
    getTemplate: function() {
          return String()
          + '<section id="redactor-modal-image">'
          + '<label>Upload image</label>'
          + '<input type="file" id="imageUpload-url">'
          + '</section>';
      },
      init: function () {
          var button = this.button.add('imageUpload', 'Image Upload');
          this.button.addCallback(button, this.imageUpload.show);

          // make your added button as Font Awesome's icon
          this.button.setAwesome('imageUpload', 'fa-image');
      },
      show: function() {
          this.modal.addTemplate('imageUpload', this.imageUpload.getTemplate());
          this.modal.load('imageUpload', 'Upload Image', 400);
          this.modal.createCancelButton();
          var button = this.modal.createActionButton('Insert');
          button.on('click', this.imageUpload.insert);
          this.selection.save();
          this.modal.show();
      },
      insert: function() {
          // var html = $('#mymodal-textarea').val();
          var html = $('#imageUpload-url').val().trim();        
          this.modal.close();
          this.selection.restore();
          this.insert.html(html);
          this.code.sync();
      }
  };
  
}


