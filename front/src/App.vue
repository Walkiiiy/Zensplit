<template>
<div>
  <div id="picArea">
  <div id="inputPic" >
    <img v-if="!showInput" src="promptPic.png" height="100" width="100" style="position: relative; top: 30vh;"> 
    <img v-if="showInput" :src="inputSrc" height="500" width="350">
  </div>
  <div id="outputPic">
    <img v-if="!showOutput && !loading" src="promptPic.png" height="100" width="100" 
    style="position: relative; top: 30vh;">
    <img v-if="loading" src="loadingPic.gif" height="100" width="100" style="position: relative; top: 30vh;"> 
    <img v-if="showOutput" @load="loadFinished" :src="outputSrc" height="500" width="350">
  </div>
  </div>
    <div style="position:absolute; right: 5vh; text-align: center;">
  <div id="introduction">
    {{ introduction }}
  </div>
  <div id="result">
    <textarea readonly v-model="result" style="background-color:rgb(35,35,35); border:none;resize: none; color: beige; width:23vw;height: 25vh;">
    </textarea>
  </div>
  </div>
  <div id="uploadButton">
<UploadImage  v-if="!loading" @upload-finished="loadimage"/>
<p v-if="loading">processing.....</p>
</div>
</div>
</template>

<script>
import axios from 'axios';
import UploadImage from './components/UploadImage.vue';
export default {
  name: 'App',
  components: {
    UploadImage,
  },
  data() {
    return {
      introduction: 'Zensplit是一个文本图片处理项目，目的在于精准分割文本图片中的字符，并返回每个字符精确的坐标。Zensplit不会存储分析您上传的图片数据。运行速度约2min/1000字',
      inputSrc: 'http://127.0.0.1:5000/inputPic',
      outputSrc:'http://127.0.0.1:5000/outputPic',  
      showInput:0,
      showOutput:0,
      loading: 0,
      result:'result'
    }
  },
  methods: {
    loadimage() {
      this.showInput = 1;
      this.showOutput = 1;
      this.loading = 1;
    },
    loadFinished() {
      this.loading = 0;
      this.getOrdinates();
    },
    getOrdinates() {
      const api = 'http://127.0.0.1:5000/ordinates';
      axios.get(api)
        .then((Response) => {
          this.result = Response.data.ordinates;
          console.log(this.result)
        })
        .catch((error) => {
          throw error
        })
    }
  },
  mounted() {
  }
}
</script>

<style>
#uploadButton{
  color: aliceblue;
  padding-top: 2%;
  text-align: center;
  background-color:black;
  height: 8vh;
  width: 28vw;
  position: fixed;
  right:1vw ;
  bottom: 1vh;
  border-radius: 5px;
  border: 1px solid darkgrey;  
}
#inputPic{
height: 95vh;
width: 35vw;
position: absolute;
left: 0;
text-align: center;
padding-top: 5vh;
border-right: 1px solid aliceblue ;
}
#outputPic{
height: 95vh;
width: 35vw;
position: absolute;
right: 0;
text-align: center;
padding-top: 5vh;
}
#picArea{
  position: absolute;
  left: 0;
  top:0;
  height: 100vh;
  width: 70vw;
  border-right: 1px solid aliceblue ;
}
#introduction{
  padding:1%;
  padding-left: 2%;
  color:darkgray;
  width:25vw;
  height: 40vh;
  border-width:1px;
  border-style: solid;
  border-color: aliceblue;
  border-radius: 5px;  
  text-align:left;
}
#result{
  padding:1%;
  margin-top: 5%;
  padding-left: 2%;
  color:darkgray;
  width:25vw;
  height: 30vh;
  border-width:1px;
  border-style: solid;
  border-color: aliceblue;
  border-radius: 5px;  
  text-align:left;
}

</style>
