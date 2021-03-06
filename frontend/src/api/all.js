import Request from '@/api/common'

// auth
import * as auths from '@/api/auths'
export const auth = auths

// systems
export const user = new Request('/sys/user/')
export const group = new Request('/sys/group/')
export const role = new Request('/sys/role/')
export const menu = new Request('/sys/menu/')
export const perm = new Request('/sys/perm/')

// tools
export const audit = new Request('/tool/audit/')
export const simple = new Request('/tool/simple/')

// notices
export const mail = new Request('/notice/mail/')
export const telegram = new Request('/notice/telegram/')

// chats
export const chatgroup = new Request('/chat/chatgroup/')
export const chatmessage = new Request('/chat/chatmessage/')

// cmdbs
export const idc = new Request('/cmdb/idc/')
export const hostgroup = new Request('/cmdb/hostgroup/')
export const host = new Request('/cmdb/host/')
export const history = new Request('/cmdb/history/')

// jenkins_tasks
import * as jenkins from '@/api/jenkins'
export const c_jenkins = jenkins
export const task = new Request('/jenkins/task/')
export const tasklog = new Request('/jenkins/tasklog/')