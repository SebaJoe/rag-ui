<template>
    <div class="row code-border">
        <div class="col zero-pad">
            <prism-editor class="my-editor" v-model="code" :highlight="highlighter"></prism-editor>
        </div>
        <div class="col-1 play-btn-col p-1 text-center">
            <button class="btn btn-dark">
                <i class="bi bi-play"></i>
            </button>
        </div>

    </div>
</template>

<script>
    // import Prism Editor
    import { PrismEditor } from 'vue-prism-editor';
    import 'vue-prism-editor/dist/prismeditor.min.css'; // import the styles somewhere

    // import highlighting library (you can use any library you want just return html string)
    import { highlight, languages } from 'prismjs/components/prism-core';
    import 'prismjs/components/prism-clike';
    import 'prismjs/components/prism-javascript';
    import 'prismjs/components/prism-python';
    import 'prismjs/themes/prism-tomorrow.css'; // import syntax highlighting styles

    export default {
        components: {
        PrismEditor,
        },
        data: () => ({ code: 'print("Hello World")' }),
        methods: {
        highlighter(code) {
            return highlight(code, languages.python); 
        },
        },
    };
    </script>

    <style>
    /* required class */
    .my-editor {
        /* we dont use `language-` classes anymore so thats why we need to add background and text color manually */
        background: #2d2d2d;
        color: #ccc;

        /* you must provide font-family font-size line-height. Example: */
        font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
        font-size: 14px;
        line-height: 1.5;
        padding: 10px;
    
    }

    .code-border {
        border: 2px solid #212529;
        border-radius: 5px;
    }

    .play-btn {
        border-radius: 1px;
    }   

    .play-btn-col {
        background-color: #212529;
    }

    .zero-pad {
        padding: 0px;
    }

    /* optional class for removing the outline */
    .prism-editor__textarea:focus {
        outline: none;
    }
</style>