"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[547],{1210:function(e,n,t){t.d(n,{Z:function(){return P}});var i=t(82394),r=t(21831),o=t(82684),l=t(47999),c=t(49894),u=t(93461),a=t(57384),s=t(41424),d=t(72454),f=t(28598);function p(e,n){var t=e.children;return(0,f.jsx)(d.HS,{ref:n,children:t})}var h=o.forwardRef(p),b=t(32063),g=t(85019),m=t(82531),y=t(66166),v=t(3055),O=t(49125),S=t(91427),I=t(24141);function j(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);n&&(i=i.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,i)}return t}function x(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?j(Object(t),!0).forEach((function(n){(0,i.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):j(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var P=function(e){var n,t=e.after,i=e.afterHidden,p=e.afterWidth,j=e.afterWidthOverride,P=e.before,N=e.beforeWidth,w=e.breadcrumbs,k=e.children,E=e.errors,Z=e.headerMenuItems,_=e.headerOffset,M=e.mainContainerHeader,C=e.navigationItems,T=e.setErrors,H=e.subheaderChildren,R=e.title,z=e.uuid,A=(0,I.i)().width,L="dashboard_after_width_".concat(z),G="dashboard_before_width_".concat(z),B=(0,o.useRef)(null),D=(0,o.useState)(j?p:(0,S.U2)(L,p)),Y=D[0],U=D[1],F=(0,o.useState)(!1),W=F[0],K=F[1],q=(0,o.useState)(P?Math.max((0,S.U2)(G,N),13*O.iI):null),Q=q[0],J=q[1],V=(0,o.useState)(!1),X=V[0],$=V[1],ee=(0,o.useState)(null)[1],ne=m.ZP.projects.list({},{revalidateOnFocus:!1}).data,te=null===ne||void 0===ne?void 0:ne.projects,ie=[];w?ie.push.apply(ie,(0,r.Z)(w)):(null===te||void 0===te?void 0:te.length)>=1&&ie.push.apply(ie,[{label:function(){var e;return null===(e=te[0])||void 0===e?void 0:e.name},linkProps:{href:"/"}},{bold:!0,label:function(){return R}}]),(0,o.useEffect)((function(){null===B||void 0===B||!B.current||W||X||null===ee||void 0===ee||ee(B.current.getBoundingClientRect().width)}),[W,Y,X,Q,B,ee,A]),(0,o.useEffect)((function(){W||(0,S.t8)(L,Y)}),[i,W,Y,L]),(0,o.useEffect)((function(){X||(0,S.t8)(G,Q)}),[X,Q,G]);var re=(0,y.Z)(p);return(0,o.useEffect)((function(){j&&re!==p&&U(p)}),[j,p,re]),(0,f.jsxs)(f.Fragment,{children:[(0,f.jsx)(a.Z,{title:R}),(0,f.jsx)(s.Z,{breadcrumbs:ie,menuItems:Z,project:null===te||void 0===te?void 0:te[0],version:null===te||void 0===te||null===(n=te[0])||void 0===n?void 0:n.version}),(0,f.jsxs)(d.Nk,{children:[0!==(null===C||void 0===C?void 0:C.length)&&(0,f.jsx)(d.lm,{showMore:!0,children:(0,f.jsx)(g.Z,{navigationItems:C,showMore:!0})}),(0,f.jsx)(u.Z,{flex:1,flexDirection:"column",children:(0,f.jsxs)(b.Z,{after:t,afterHeightOffset:v.Mz,afterHidden:i,afterMousedownActive:W,afterWidth:Y,before:P,beforeHeightOffset:v.Mz,beforeMousedownActive:X,beforeWidth:d.k1+(P?Q:0),headerOffset:_,hideAfterCompletely:!0,leftOffset:P?d.k1:null,mainContainerHeader:M,mainContainerRef:B,setAfterMousedownActive:K,setAfterWidth:U,setBeforeMousedownActive:$,setBeforeWidth:J,children:[H&&(0,f.jsx)(h,{children:H}),k]})})]}),E&&(0,f.jsx)(l.Z,{disableClickOutside:!0,isOpen:!0,onClickOutside:function(){return null===T||void 0===T?void 0:T(null)},children:(0,f.jsx)(c.Z,x(x({},E),{},{onClose:function(){return null===T||void 0===T?void 0:T(null)}}))})]})}},59920:function(e,n,t){var i;t.d(n,{M:function(){return i}}),function(e){e.BACKFILLS="backfills",e.BLOCK_RUNS="block_runs",e.EDIT="edit",e.MONITOR="monitor",e.PIPELINE_LOGS="pipeline_logs",e.PIPELINE_RUNS="pipeline_runs",e.RUNS="runs",e.SETTINGS="settings",e.SYNCS="syncs",e.TRIGGERS="triggers"}(i||(i={}))},60547:function(e,n,t){t.d(n,{Z:function(){return w}});var i=t(82394),r=t(21831),o=t(82684),l=t(34376),c=t(47999),u=t(1210),a=t(34744),s=t(49894),d=t(67971),f=t(87372),p=t(86673),h=t(82531),b=t(38626),g=t(23831),m=t(73942),y=t(49125),v=b.default.div.withConfig({displayName:"indexstyle__BannerStyle",componentId:"sc-1te3pmf-0"})(["border-radius:","px;padding:","px;"," "," ",""],m.n_,3*y.iI,(function(e){return"\n    box-shadow: ".concat((e.theme.shadow||g.Z.shadow).small,";\n  ")}),(function(e){return e.background&&"\n    background: ".concat(e.background,";\n  ")}),(function(e){return e.backgroundImage&&'\n    background-image: url("'.concat(e.backgroundImage,'");\n    background-position: center;\n    background-repeat: no-repeat;\n    background-size: cover;\n  ')})),O=t(3055),S=t(36405),I=t(96510),j=t(24141),x=t(28598);function P(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);n&&(i=i.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,i)}return t}function N(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?P(Object(t),!0).forEach((function(n){(0,i.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):P(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var w=function(e){var n=e.after,t=e.afterHidden,i=e.afterWidth,b=e.before,g=e.beforeWidth,m=e.breadcrumbs,P=e.buildSidekick,w=e.children,k=e.errors,E=e.headline,Z=e.pageName,_=e.pipeline,M=e.setErrors,C=e.subheader,T=e.subheaderBackground,H=e.subheaderBackgroundImage,R=e.subheaderButton,z=e.subheaderText,A=e.title,L=e.uuid,G=(0,j.i)().height,B=(0,l.useRouter)().query.pipeline,D=_.uuid,Y=h.ZP.pipelines.detail(D,{includes_outputs:!1},{revalidateOnFocus:!1}).data,U=null===Y||void 0===Y?void 0:Y.pipeline;(0,o.useEffect)((function(){(0,I.bB)(Y,M)}),[Y,M]);var F=(0,o.useMemo)((function(){return n||(P?P({height:G,heightOffset:O.Mz,pipeline:U}):null)}),[n,P,G,U]),W=i||(F?50*y.iI:null),K=(0,o.useMemo)((function(){var e=[];return U?(e.push.apply(e,[{label:function(){return"Pipelines"},linkProps:{href:"/pipelines"}}]),m?(e.push({label:function(){return U.uuid},linkProps:{as:"/pipelines/".concat(D,"/triggers"),href:"/pipelines/[pipeline]/triggers"}}),e.push.apply(e,(0,r.Z)(m)),e[e.length-1].bold=!0):e.push({bold:!0,label:function(){return U.name}})):null!==Y&&void 0!==Y&&Y.error&&e.push({bold:!0,danger:!0,label:function(){return"Error loading pipeline"}}),e}),[m,null===Y||void 0===Y?void 0:Y.error,U,D]);return(0,x.jsxs)(x.Fragment,{children:[(0,x.jsxs)(u.Z,{after:F,afterHidden:t,afterWidth:W,before:b,beforeWidth:g,breadcrumbs:K,navigationItems:(0,S.H)(Z,U,B),subheaderChildren:"undefined"!==typeof C&&C,title:U?A?A(U):U.name:null,uuid:L,children:[(R||z)&&(0,x.jsx)(p.Z,{mb:y.Mq,mt:y.cd,mx:y.cd,children:(0,x.jsx)(v,{background:T,backgroundImage:H,children:(0,x.jsxs)(d.Z,{alignItems:"center",children:[R,z&&(0,x.jsx)(p.Z,{ml:3}),z]})})}),E&&(0,x.jsx)(p.Z,{p:y.cd,children:(0,x.jsxs)(p.Z,{mt:y.cd,px:y.cd,children:[(0,x.jsx)(f.Z,{level:5,children:E}),(0,x.jsx)(a.Z,{light:!0,mt:y.cd,short:!0})]})}),w]}),k&&(0,x.jsx)(c.Z,{disableClickOutside:!0,isOpen:!0,onClickOutside:function(){return null===M||void 0===M?void 0:M(null)},children:(0,x.jsx)(s.Z,N(N({},k),{},{onClose:function(){return null===M||void 0===M?void 0:M(null)}}))})]})}},36405:function(e,n,t){t.d(n,{H:function(){return c}});var i=t(98781),r=t(10503),o=t(59920),l=t(9736);function c(e,n,t){var c=(n||{}).uuid||t,u=[{Icon:r.Bf,id:o.M.TRIGGERS,isSelected:function(){return o.M.TRIGGERS===e},label:function(){return"Triggers"},linkProps:{as:"/pipelines/".concat(c,"/triggers"),href:"/pipelines/[pipeline]/triggers"}},{Icon:r.Pf,id:o.M.RUNS,isSelected:function(){return o.M.RUNS===e},label:function(){return"Runs"},linkProps:{as:"/pipelines/".concat(c,"/runs"),href:"/pipelines/[pipeline]/runs"}},{Icon:r.dE,id:o.M.BACKFILLS,isSelected:function(){return o.M.BACKFILLS===e},label:function(){return"Backfills"},linkProps:{as:"/pipelines/".concat(c,"/backfills"),href:"/pipelines/[pipeline]/backfills"}},{Icon:r.UL,id:o.M.PIPELINE_LOGS,isSelected:function(){return o.M.PIPELINE_LOGS===e},label:function(){return"Logs"},linkProps:{as:"/pipelines/".concat(c,"/logs"),href:"/pipelines/[pipeline]/logs"}},{Icon:r.ug,id:o.M.MONITOR,isSelected:function(){return o.M.MONITOR===e},label:function(){return"Monitor"},linkProps:{as:"/pipelines/".concat(c,"/monitors"),href:"/pipelines/[pipeline]/monitors"}}];return i.qL.INTEGRATION===(null===n||void 0===n?void 0:n.type)&&u.unshift({Icon:r.Nt,id:o.M.SYNCS,isSelected:function(){return o.M.SYNCS===e},label:function(){return"Syncs"},linkProps:{as:"/pipelines/".concat(c,"/syncs"),href:"/pipelines/[pipeline]/syncs"}}),(0,l.Ct)()||(u.unshift({Icon:r.EK,disabled:!c,id:o.M.EDIT,isSelected:function(){return o.M.EDIT===e},label:function(){return"Edit pipeline"},linkProps:{as:"/pipelines/".concat(c,"/edit"),href:"/pipelines/[pipeline]/edit"}}),u.push({Icon:r.Zr,id:o.M.SETTINGS,isSelected:function(){return o.M.SETTINGS===e},label:function(){return"Pipeline settings"},linkProps:{as:"/pipelines/".concat(c,"/settings"),href:"/pipelines/[pipeline]/settings"}})),u}},98781:function(e,n,t){t.d(n,{$1:function(){return u},G7:function(){return s},QK:function(){return c},a_:function(){return d},qL:function(){return o},r0:function(){return a}});var i,r,o,l=t(82394);!function(e){e.INTEGRATION="integration",e.PYTHON="python",e.PYSPARK="pyspark",e.STREAMING="streaming"}(o||(o={}));var c,u,a,s=(i={},(0,l.Z)(i,o.INTEGRATION,"Integration"),(0,l.Z)(i,o.PYTHON,"Standard"),(0,l.Z)(i,o.PYSPARK,"PySpark"),(0,l.Z)(i,o.STREAMING,"Streaming"),i);!function(e){e.ACTIVE="active",e.INACTIVE="inactive",e.NO_SCHEDULES="no_schedules",e.RETRY="retry"}(c||(c={})),function(e){e.GROUP="group_by",e.STATUS="status[]",e.TYPE="type[]"}(u||(u={})),function(e){e.STATUS="status",e.TYPE="type"}(a||(a={}));var d=(r={},(0,l.Z)(r,o.PYTHON,"python3"),(0,l.Z)(r,o.PYSPARK,"pysparkkernel"),r)},87372:function(e,n,t){var i,r,o,l,c,u,a,s,d=t(82394),f=t(26304),p=t(26653),h=t(38626),b=t(33591),g=t(23831),m=t(2005),y=t(31012),v=t(19711),O=t(49125),S=t(86673),I=t(28598),j=["children","condensed","inline","level","marketing","spacingBelow"];function x(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);n&&(i=i.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,i)}return t}function P(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?x(Object(t),!0).forEach((function(n){(0,d.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):x(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var N=(0,h.css)([""," margin:0;"," "," "," "," "," "," "," "," "," "," "," "," ",""],v.IH,(function(e){return e.color&&"\n    color: ".concat(e.color,"\n  ")}),(function(e){return e.yellow&&"\n    color: ".concat((e.theme.accent||g.Z.accent).yellow,";\n  ")}),(function(e){return e.center&&"\n    text-align: center;\n  "}),(function(e){return!e.monospace&&0===Number(e.weightStyle)&&"\n    font-family: ".concat(m.iI,";\n  ")}),(function(e){return!e.monospace&&1===Number(e.weightStyle)&&"\n    font-family: ".concat(m.LX,";\n  ")}),(function(e){return!e.monospace&&2===Number(e.weightStyle)&&"\n    font-family: ".concat(m.LX,";\n  ")}),(function(e){return!e.monospace&&3===Number(e.weightStyle)&&"\n    font-family: ".concat(m.ry,";\n  ")}),(function(e){return!e.monospace&&4===Number(e.weightStyle)&&"\n    font-family: ".concat(m.YC,";\n  ")}),(function(e){return!e.monospace&&5===Number(e.weightStyle)&&"\n    font-family: ".concat(m.nF,";\n  ")}),(function(e){return!e.monospace&&(6===Number(e.weightStyle)||e.bold)&&"\n    font-family: ".concat(m.nF,";\n  ")}),(function(e){return!e.monospace&&7===Number(e.weightStyle)&&"\n    font-family: ".concat(m.nF,";\n  ")}),(function(e){return!e.monospace&&8===Number(e.weightStyle)&&"\n    font-family: ".concat(m.nF,";\n  ")}),(function(e){return e.lineHeightAuto&&"\n    line-height: normal !important;\n  "})),w=h.default.div.withConfig({displayName:"Headline__HeadlineContainerStyle",componentId:"sc-12jzt2e-0"})(["",""],(function(e){return"\n    color: ".concat((e.theme.content||g.Z.content).active,";\n  ")})),k=h.default.h1.withConfig({displayName:"Headline__H1HeroStyle",componentId:"sc-12jzt2e-1"})([""," font-size:42px;line-height:56px;"," "," ",""],N,b.media.md(i||(i=(0,p.Z)(["\n    ","\n  "])),y.aQ),b.media.lg(r||(r=(0,p.Z)(["\n    ","\n  "])),y.aQ),b.media.xl(o||(o=(0,p.Z)(["\n    ","\n  "])),y.aQ)),E=h.default.h1.withConfig({displayName:"Headline__H1Style",componentId:"sc-12jzt2e-2"})([""," ",""],N,y.MJ),Z=h.default.h1.withConfig({displayName:"Headline__H1MarketingStyle",componentId:"sc-12jzt2e-3"})([""," "," "," "," "," ",""],N,b.media.xs(l||(l=(0,p.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*O.iI,7*O.iI),b.media.sm(c||(c=(0,p.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*O.iI,7*O.iI),b.media.md(u||(u=(0,p.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*O.iI,7*O.iI),b.media.lg(a||(a=(0,p.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*O.iI,7*O.iI),b.media.xl(s||(s=(0,p.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*O.iI,7*O.iI)),_=h.default.h2.withConfig({displayName:"Headline__H2Style",componentId:"sc-12jzt2e-4"})([""," ",""],N,y.BL),M=h.default.h3.withConfig({displayName:"Headline__H3Style",componentId:"sc-12jzt2e-5"})([""," font-size:24px;line-height:32px;"],N),C=h.default.h4.withConfig({displayName:"Headline__H4Style",componentId:"sc-12jzt2e-6"})([""," font-size:20px;line-height:28px;"],N),T=h.default.h5.withConfig({displayName:"Headline__H5Style",componentId:"sc-12jzt2e-7"})([""," font-size:18px;line-height:26px;"],N),H=h.default.span.withConfig({displayName:"Headline__SpanStyle",componentId:"sc-12jzt2e-8"})([""," "," "," "," ",""],N,(function(e){return 1===e.level&&"\n    ".concat(y.MJ,"\n  ")}),(function(e){return 2===e.level&&"\n    ".concat(y.BL,"\n  ")}),(function(e){return 3===e.level&&"\n    font-size: 24px;\n    line-height: 32px;\n  "}),(function(e){return 4===e.level&&"\n    font-size: 20px;\n    line-height: 28px;\n  "})),R=function(e){var n,t=e.children,i=e.condensed,r=e.inline,o=e.level,l=e.marketing,c=e.spacingBelow,u=(0,f.Z)(e,j);r?n=H:0===Number(o)?n=k:1===Number(o)?n=l?Z:E:2===Number(o)?n=_:3===Number(o)?n=M:4===Number(o)?n=C:5===Number(o)&&(n=T);var a=(0,I.jsxs)(n,P(P({},u),{},{level:o,children:[c&&(0,I.jsx)(S.Z,{mb:i?2:3,children:t}),!c&&t]}));return r?a:(0,I.jsx)(w,{children:a})};R.defaultProps={level:3,weightStyle:6},n.Z=R}}]);