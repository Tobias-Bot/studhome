import VueRouter from "vue-router";

import login from "./pages/login";

import home from "./pages/home";
import profile from "./pages/home/profile";
import bookmarks from "./pages/home/bookmarks";
import settings from "./pages/home/settings";

import news from "./pages/news";
import all_posts from "./pages/news/pages/all_posts";
import full_post from "./components/full_post";
import full_pic from "./components/full_pic";
import my_news from "./pages/news/pages/my_news";

import GlobalSearch from "./pages/GlobalSearch";

import create_post from "./pages/create_post";
// home import
// const home = resolve => {
//     require.ensure(['./pages/home.vue'], () => {
//         resolve(
//             require('./pages/home.vue')
//         )
//     })
// }

// apps import
// const apps = resolve => {
//     require.ensure(['./pages/apps.vue'], () => {
//         resolve(
//             require('./pages/apps.vue')
//         )
//     })
// }

// chatroom import
// const chatroom = resolve => {
//     require.ensure(['./pages/chatroom.vue'], () => {
//         resolve(
//             require('./pages/chatroom.vue')
//         )
//     })
// }

// news import
// const news = resolve => {
//     require.ensure(['./pages/news.vue'], () => {
//         resolve(
//             require('./pages/news.vue')
//         )
//     })
// }

// settings import
// const settings = resolve => {
//     require.ensure(['./pages/settings.vue'], () => {
//         resolve(
//             require('./pages/settings.vue')
//         )
//     })
// }

const router = new VueRouter({
  routes: [
    {
      name: "CreatePost",
      path: "/whatsnew",
      component: create_post
    },
    {
      name: "login",
      path: "/login",
      component: login
    },
    {
      name: "home",
      path: "/home",
      component: home,
      children: [
        {
          name: "bookmarks",
          path: "bookmarks",
          component: bookmarks
        },
        {
          name: "settings",
          path: "settings",
          component: settings
        },
      ]
    },
    {
      name: "profile",
      path: "/profile_:username",
      component: profile
    },
    {
      name: "news",
      path: "/news",
      component: news,
      children: [
        {
          name: "MyNews",
          path: "me",
          component: my_news
        },
        {
          name: "AllPosts",
          path: "main",
          component: all_posts
        },
      ]
    },
    {
      name: "post",
      path: "/post_:post_id",
      component: full_post
    },
    {
      name: "pic",
      path: "/pic_:post_id:pic_id",
      component: full_pic
    },
    {
      name: "GlobalSearch",
      path: "/search",
      component: GlobalSearch
    },
    {
      name: "others",
      path: "*",
      redirect: ""
    }
  ],
  mode: "history"
});

router.beforeEach((to, from, next) => {
  let isAuthenticated = localStorage.getItem("token");

  if (!isAuthenticated) {
    if (to.name !== "login") next({ name: "login" });
    else next();
  }
  else {
    if (to.name == "login" && from.name !== "settings") next({ name: "home" });
    else next();
  }
});

export default router;
