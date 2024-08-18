import{_ as v}from"./Breadcrum-DcrIbtRq.js";import{L as f,M as h,r as _,N as g,z as u,c as E,A as l,B as s,E as C,G as a,H as y,F as w,a as k,I as p,o as B,u as D}from"./index-DX0kaMnH.js";import"./2-BQBUVaIZ.js";const L="/assets/single-course-thumb-CEZExon1.png",N="/assets/account-CaxZmnB2.png",T={class:"xl:max-w-[1350px] lg:max-w-[960px] md:max-w-2xl sm:max-w-xl xl mx-auto px-3 py-20"},A={class:"container mx-auto"},M={class:"grid grid-cols-12 gap-[30px]"},I={class:"lg:col-span-8 col-span-12"},S={class:"single-course-details"},V=s("div",{class:"xl:h-[470px] h-[350px] mb-10 course-main-thumb"},[s("img",{src:L,alt:"",class:"rounded-md object-fut w-full h-full block"})],-1),z=s("div",{class:"mb-6"},[s("span",{class:"bg-devanga-secondary py-1 px-3 font-raleway font-semibold rounded text-white"},"Data Science")],-1),F={class:"enrolled mb-6 h-48 w-32"},G={class:"font-raleway text-4xl font-semibold"},H={class:"author-meta mt-6 sm:flex lg:space-x-16 sm:space-x-5 space-y-5 sm:space-y-0 items-center"},$={class:"flex space-x-4 items-center group"},Z={class:"flex-1"},j={class:"text-devanga-secondary"},P={href:"#",class:"text-black"},R={class:"text-secondary"},U={id:"tab1",class:"tab-content",style:{}},W={class:"py-4"},q=s("h3",{class:"font-bold font-raleway text-2xl"},"Course Description",-1),J=["innerHTML"],K={class:"lg:col-span-4 col-span-12"},O={class:"sidebarWrapper space-y-[30px]"},Q={class:"wdiget custom-text space-y-5"},X={class:"font-bold font-raleway text-2xl"},Y={class:"list"},ss={class:"flex space-x-3 border-b border-[#ECECEC] mb-4 pb-4 last:pb-0 past:mb-0 last:border-0"},es=s("div",{class:"flex-1 space-x-3 flex"},[s("img",{src:"",alt:""}),s("div",{class:"text-black font-semibold"},"Instructor")],-1),ts={class:"flex-none"},as={class:"flex space-x-3 border-b border-[#ECECEC] mb-4 pb-4 last:pb-0 past:mb-0 last:border-0"},ls=s("div",{class:"flex-1 space-x-3 flex"},[s("img",{src:"",alt:""}),s("div",{class:"text-black font-semibold"},"Modules")],-1),os={class:"flex-none"},cs={class:"flex space-x-3 border-b border-[#ECECEC] mb-4 pb-4 last:pb-0 past:mb-0 last:border-0"},ns=s("div",{class:"flex-1 space-x-3 flex"},[s("img",{src:"",alt:""}),s("div",{class:"text-black font-semibold"},"Enrolled")],-1),rs={class:"flex-none"},is=k('<li class="flex space-x-3 border-b border-[#ECECEC] mb-4 pb-4 last:pb-0 past:mb-0 last:border-0"><div class="flex-1 space-x-3 flex"><img src="" alt=""><div class="text-black font-semibold">Course level</div></div><div class="flex-none"> Intermediate </div></li><li class="flex space-x-3 border-b border-[#ECECEC] mb-4 pb-4 last:pb-0 past:mb-0 last:border-0"><div class="flex-1 space-x-3 flex"><img src="" alt=""><div class="text-black font-semibold">Language</div></div><div class="flex-none"> English </div></li>',2),bs={__name:"CourseDetail",setup(ds){const o=f(),c=h().params.slug,e=_([]),n=_(!1),x=()=>{p.get(`course/courses/${c}/`).then(t=>{e.value=t.data,o.add({severity:"success",summary:"Successful",detail:"Course Deleted",life:3e3})}).catch(t=>{console.error("Error deleting course:",t),o.add({severity:"error",summary:"Error",detail:"Error deleting course",life:3e3})})},m=async()=>{n.value=!0;try{const t=await p.post(`/course/${c}/enroll/`,{});console.log("Enrollment successful:",t.data)}catch(t){console.error("Enrollment failed:",t),enrollmentError.value="Failed to enroll. Please try again later."}finally{n.value=!1}};return g(()=>{x()}),(t,us)=>{const r=u("Avatar"),b=u("AvatarGroup");return B(),E(w,null,[l(v),s("div",T,[s("div",A,[s("div",M,[s("div",I,[s("div",S,[V,z,s("div",F,[l(b,{class:"mr--4"},{default:C(()=>{var i,d;return[l(r,{image:D(N),size:"normal",shape:"circle"},null,8,["image"]),l(r,{label:((d=(i=e.value)==null?void 0:i.enrollments)==null?void 0:d.length)+"Enrollment(s)",shape:"circle",size:"large"},null,8,["label"])]}),_:1})]),s("h2",G,a(e.value.title),1),s("div",H,[s("div",$,[s("div",Z,[s("span",j,[y("Trainer "),s("a",P," : "+a(e.value.instructor.full_name),1)])])]),s("div",null,[s("span",R,"Last Update: "+a(e.value.updated_at),1)])]),s("div",U,[s("div",W,[q,s("div",{class:"",innerHTML:e.value.description},null,8,J)])])])]),s("div",K,[s("div",O,[s("div",Q,[s("h3",X,"Tsh "+a(e.value.price),1),s("div",{class:""},[s("button",{class:"btn bg-devanga-secondary text-white p-4 rounded-sm w-full text-center text-xl font-bold",onClick:m}," Enroll Now ")]),s("ul",Y,[s("li",ss,[es,s("div",ts,a(e.value.instructor.full_name),1)]),s("li",as,[ls,s("div",os,a(e.value.modules.length),1)]),s("li",cs,[ns,s("div",rs,a(e.value.enrollments.length),1)]),is])])])])])])])],64)}}};export{bs as default};