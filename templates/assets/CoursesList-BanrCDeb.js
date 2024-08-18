import{_ as j}from"./Breadcrum-DcrIbtRq.js";import{r as p,e as B,z as c,c as n,A as t,B as s,E as a,F as _,I as C,o as i,K as h,C as b,G as l}from"./index-DX0kaMnH.js";import"./2-BQBUVaIZ.js";const T={class:"container mx-auto py-36"},L={class:"flex justify-end"},S={class:"flex flex-col"},D={class:"md:w-40 relative"},E=["src","alt"],M={class:"flex flex-col md:flex-row justify-between md:items-center flex-1 gap-6"},z={class:"flex flex-row md:flex-col justify-between items-start gap-2"},F={class:"font-medium text-surface-500 dark:text-surface-400 text-sm"},H={class:"text-lg font-medium mt-2"},I={class:"bg-surface-100 p-1",style:{"border-radius":"30px"}},N={class:"bg-surface-0 flex items-center gap-2 justify-center py-1 px-2",style:{"border-radius":"30px","box-shadow":`0px 1px 2px 0px rgba(0, 0, 0, 0.04),
                                0px 1px 2px 0px rgba(0, 0, 0, 0.06)`}},A={class:"text-surface-900 font-medium text-sm"},G=s("i",{class:"pi pi-star-fill text-yellow-500"},null,-1),K={class:"flex flex-col md:items-end gap-8"},U={class:"text-xl font-semibold"},$={class:"flex flex-row-reverse md:flex-row gap-2"},q={class:"grid grid-cols-12 gap-4"},J={class:"p-6 border border-surface-200 dark:border-surface-700 bg-surface-0 dark:bg-surface-900 rounded flex flex-col"},O={class:"bg-surface-50 flex justify-center rounded p-4"},P={class:"relative mx-auto"},Q=["src","alt"],R={class:"pt-6"},W={class:"flex flex-row justify-between items-start gap-2"},X={class:"font-medium text-surface-500 dark:text-surface-400 text-sm"},Y=["innerHTML"],Z={class:"text-lg font-medium mt-1"},ss={class:"bg-surface-100 p-1",style:{"border-radius":"30px"}},es={class:"bg-surface-0 flex items-center gap-2 justify-center py-1 px-2",style:{"border-radius":"30px","box-shadow":`0px 1px 2px 0px rgba(0, 0, 0, 0.04),
                                0px 1px 2px 0px rgba(0, 0, 0, 0.06)`}},ts={class:"text-surface-900 font-medium text-sm"},os=s("i",{class:"pi pi-star-fill text-yellow-500"},null,-1),ls={class:"flex flex-col gap-6 mt-6"},as={class:"text-2xl font-semibold"},cs={class:"flex gap-2 justify-center"},us={__name:"CoursesList",setup(ns){const x=p({}),u=p("grid"),y=p(["list","grid"]),w=()=>{C.get("course/courses/").then(r=>{x.value=r.data}).catch(r=>{console.log(r)})};return B(()=>{w()}),(r,f)=>{const k=c("SelectButton"),m=c("Tag"),v=c("Button"),g=c("router-link"),V=c("DataView");return i(),n(_,null,[t(j),s("div",T,[t(V,{value:x.value,layout:u.value},{header:a(()=>[s("div",L,[t(k,{modelValue:u.value,"onUpdate:modelValue":f[0]||(f[0]=o=>u.value=o),options:y.value,allowEmpty:!1},{option:a(({option:o})=>[s("i",{class:h([o==="list"?"pi pi-bars":"pi pi-table"])},null,2)]),_:1},8,["modelValue","options"])])]),list:a(o=>[s("div",S,[(i(!0),n(_,null,b(o.items,(e,d)=>(i(),n("div",{key:d},[s("div",{class:h(["flex flex-col sm:flex-row sm:items-center p-6 gap-4",{"border-t border-surface-200 dark:border-surface-700":d!==0}])},[s("div",D,[s("img",{class:"block xl:block mx-auto rounded w-full",src:e.cover,alt:e.title},null,8,E),t(m,{value:e.inventoryStatus,class:"absolute dark:!bg-surface-900",style:{left:"4px",top:"4px"}},null,8,["value"])]),s("div",M,[s("div",z,[s("div",null,[s("span",F,l(e.category),1),s("div",H,l(e.title),1)]),s("div",I,[s("div",N,[s("span",A,l(e.rating),1),G])])]),s("div",K,[s("span",U,"Tsh "+l(e.price),1),s("div",$,[t(g,{to:{name:"coaching-detail",params:{slug:e.slug}}},{default:a(()=>[t(v,{icon:"pi pi-eye",severity:"info",label:"View Course"})]),_:2},1032,["to"])])])])],2)]))),128))])]),grid:a(o=>[s("div",q,[(i(!0),n(_,null,b(o.items,(e,d)=>(i(),n("div",{key:d,class:"col-span-12 sm:col-span-6 md:col-span-4 xl:col-span-4 p-2"},[s("div",J,[s("div",O,[s("div",P,[s("img",{class:"rounded w-full",src:e.cover,alt:e.title,style:{"max-width":"300px"}},null,8,Q),t(m,{value:e.event_type,class:"absolute dark:!bg-surface-900",style:{left:"4px",top:"4px"}},null,8,["value"])])]),s("div",R,[s("div",W,[s("div",null,[s("span",X,[s("div",{class:"text-clip",innerHTML:e.description},null,8,Y)]),s("div",Z,l(e.title),1)]),s("div",ss,[s("div",es,[s("span",ts,l(e.rating),1),os])])]),s("div",ls,[s("span",as,"Tsh "+l(e.price),1),s("div",cs,[t(g,{to:{name:"coaching-detail",params:{slug:e.slug}}},{default:a(()=>[t(v,{icon:"pi pi-eye",severity:"info",label:"View Course"})]),_:2},1032,["to"])])])])])]))),128))])]),_:1},8,["value","layout"])])],64)}}};export{us as default};
