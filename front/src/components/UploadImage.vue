<template>
<div class="center">
  <vue-core-image-upload
    class="btn btn-primary"
    :crop="false"
    :max-file-size="5242880"
    url="http://127.0.0.1:5000/uploadPic" 
    @imageuploaded="onImageUploaded">
  </vue-core-image-upload>
</div>
</template>

<script>
import VueCoreImageUpload from 'vue-core-image-upload'
export default {
  components: {
    'vue-core-image-upload': VueCoreImageUpload,
  },
  data() {
    return {
    }
  },
  methods: {
    onImageUploaded(response) {
      // 处理上传完成后的逻辑
      // 然后触发自定义事件
      this.$emit('upload-finished', response);
    }
  }
}
</script>