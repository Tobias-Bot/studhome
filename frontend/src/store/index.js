import Vue from 'vue'
import Vuex from 'vuex'
import home from './home'
import news from './news'
import settings from './settings'
import authorization from './authorization'
import TextEditor from './apps/TextEditor'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        settings,
        authorization,
        home,
        news,
        
        TextEditor,
    }
});