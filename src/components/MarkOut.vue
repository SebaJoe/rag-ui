
<template>
    <div @mouseover="show_options=true" @mouseleave="(!edit_mode) ? show_options=false : show_options">
        <div class="options-bar" v-if="show_options">
            <div class="container">
                <div class="row" @click="edit_cell()">
                    <div class="col" v-if="edit_mode">
                        <i class="bi bi-pencil-fill clickable"></i>
                    </div>
                    <div class="col" v-else>
                        <i class="bi bi-pencil-fill clickable text-muted"></i>
                    </div>
                </div>
                <div class="row" @click="cancel_changes()" v-if="edit_mode">
                    <div class="col">
                        <i class="bi bi-x"></i>
                    </div>
                </div>
            </div>
        </div>
        <div ref="mark_view_box" class="radial" :class="{user_class:isUser}">
            <textarea ref="mark_edit_box" class="edit_box" v-model="temp_text" v-show="edit_mode" @keydown.ctrl.enter.prevent="edit_cell()" autofocus></textarea>
            <vue-markdown :class="{remove_margin:isUser}" v-show="!edit_mode" :source="text" :options="md_options" />
        </div>
    </div>
</template>


<script>

    import VueMarkdown from 'vue-markdown-render';

    import hljs from 'highlight.js';

    export default {
        components: {
            VueMarkdown
        },
        props: {
            text: {required: true, type: String},
            isUser: {default: false, type: Boolean},
            start_edit: {default: false, type: Boolean},
        },
        mounted () {
            if (this.start_edit) {
                this.edit_cell();
            }
        },
        data () {

            var defaults = {
                    html: true,
                    typographer: true,
                    _highlight: true, // <= THIS IS WHAT YOU NEED
                };

                defaults.highlight = function (str, lang) {
                    if (lang && hljs.getLanguage(lang)) {
                        try {
                            return hljs.highlight(str, { language: lang }).value;
                        } catch (__) {}
                    }

                    return ''; // use external default escaping
                }

                return {
                    md_options: defaults,
                    show_options: false,
                    edit_mode: false,
                    temp_text: this.text,
                }
        },
        methods: {
            edit_cell() {
                if (this.edit_mode) {
                    this.$emit('update:text', this.temp_text);
                    this.edit_mode = false;
                    this.show_options = false;
                } else {
                    this.temp_text = this.text;
                    let save_height = this.$refs.mark_view_box.offsetHeight;
                    console.log(this.$refs);
                    console.log(save_height);
                    this.edit_mode = true;
                    this.show_options = true;
                    console.log(save_height);
                    if (this.$refs.mark_edit_box) {
                        console.log("Help Me");
                        this.$refs.mark_edit_box.style.height = `${save_height}px`;
                    }
                }
            },
            cancel_changes() {
                this.edit_mode = false;
                this.temp_text = this.text;
            },
        }
    }
</script>

<style>


.edit_box {
    border: none;
    overflow: auto;
    outline: none;

    font-family: 'Courier New', Courier, monospace;

    -webkit-box-shadow: none;
    -moz-box-shadow: none;
    box-shadow: none;

    resize: none; /*remove the resize handle on the bottom right*/

    width: 100%;
}

.radial {
    border-radius: 10px;
    padding: 10px;
}

.user_class {
    background-color:  #a9cce3;
    border: 5px solid  #1a5276;
}

.remove_margin > p {
    margin: 0px;
}

.options-bar {
    position: absolute;
    width: 30px;
    left: 74%;
}

.clickable {
    cursor: pointer;
}

</style>