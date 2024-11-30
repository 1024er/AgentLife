import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { nightOwl } from 'react-syntax-highlighter/dist/esm/styles/prism';


const EventBox = ({
    characters,
    selectedAvatar
}) => {
    const event = characters?.find(character => character.id === selectedAvatar)?.event
    
    if (!event) {
        return null
    }

    return (
        <>
            {event.type === "book" && (
                <div className="fixed right-5 bottom-5 w-80 h-2/5 flex p-0 bg-opacity-30 shadow-lg backdrop-blur-sm duration-500" style={{ userSelect: 'none' }}>
                    <header className="bg-gray-600 bg-opacity-30 p-4 flex items-center justify-center text-base text-sky-50">
                        <div className="breathing-light align-middle" style={{writingMode: 'vertical-rl'}}>
                        📖 &nbsp; 正在阅读 { event.book_name }
                        </div>
                    </header>
                    <article class="text-xs text-sky-50 p-4 overflow-y-auto"  style={{ whiteSpace: 'pre-line' }}>
                        {event.paragraphs[0].title} <br /> <br />
                        {event.paragraphs[0].content}
                    </article>
                </div>
            )}

            {event.type === "news" && (
                <div className="fixed right-5 bottom-5 w-80 h-2/5 flex p-0 bg-opacity-30 shadow-lg backdrop-blur-sm duration-500" style={{ userSelect: 'none' }}>
                    <header className="bg-gray-600 bg-opacity-30 p-4 flex items-center justify-center text-base text-sky-50">
                        <div className="breathing-light align-middle" style={{writingMode: 'vertical-rl'}}>
                        🌐 &nbsp; 网上冲浪中
                        </div>
                    </header>

                    <article className="text-sky-50 p-4 overflow-y-auto"  style={{ whiteSpace: 'pre-line' }}>
                        <p className="text-sm font-bold">{event.contents[0].title}</p>
                        
                        <hr className="my-2 border-t border-gray-300" />

                        <div className="flex items-center space-x-2">
                            { event.contents[0].publisher_avatar_url != "" &&
                                <img className='rounded-full w-8' src={event.contents[0].publisher_avatar_url} />
                            }
                            <div className="flex flex-col">
                                <p className="text-xs text-gray-200/70">{event.contents[0].publisher_name}</p>
                                <p className="text-xs text-gray-200/70">{event.contents[0].publish_time}</p>
                            </div>
                        </div>

                        <p className="text-xs py-2 text-sky-50">{event.contents[0].content}</p>
                        <p className="text-xs text-gray-200/70">阅读量：{event.contents[0].read_count}</p>
                    </article>
                </div>
            )}

            {event.type === "find_geek_news" && (
                <div className="fixed right-5 bottom-5 w-80 h-2/5 flex p-0 bg-opacity-30 shadow-lg backdrop-blur-sm duration-500" style={{ userSelect: 'none' }}>
                    <header className="bg-gray-600 bg-opacity-30 p-4 flex items-center justify-center text-base text-sky-50">
                        <div className="breathing-light align-middle" style={{writingMode: 'vertical-rl'}}>
                        💻 &nbsp; Geek 时间
                        </div>
                    </header>

                    <article class="text-xs text-sky-50 p-4 overflow-y-auto overflow-x-hidden"  style={{ whiteSpace: 'pre-line' }}>
                        {event.contents.map((result, index) => (
                            <div key={index}>
                                <div className="flex space-x-2 py-2">
                                    { result.publisher_avatar_url !== "" && <div>
                                        <img className='w-10 rounded-full' src={result.publisher_avatar_url} />
                                    </div>
                                    }
                                    <div>
                                        <p className="text-xs font-bold">[稀土掘金] {result.title}</p>
                                    </div>
                                </div>
                                
                                <div className="flex space-x-2 m-1">
                                    <p className="text-xs text-gray-200/90 truncate">{result.tags.join('-')}</p>
                                    <p className="text-xs text-gray-200/90">{result.read_time}</p>
                                </div>

                                <p className="text-xs text-gray-100">{result.abstract}</p>

                                <div className="flex space-x-2 py-2">
                                    <p className="text-xs text-gray-200/90">{result.publish_time}</p>
                                    <p className="text-xs text-gray-200/90">阅读量：{result.read_count}</p>
                                </div>

                                <hr className="my-2 border-t border-gray-300" />
                            </div>
                        ))}
                    </article>
                </div>
            )}

            {event.type === "read_geek_news" && (
                <div className="fixed right-5 bottom-5 w-80 h-2/5 flex p-0 bg-opacity-30 shadow-lg backdrop-blur-sm duration-500" style={{ userSelect: 'none' }}>
                    <header className="bg-gray-600 bg-opacity-30 p-4 flex items-center justify-center text-base text-sky-50">
                        <div className="breathing-light align-middle" style={{writingMode: 'vertical-rl'}}>
                        💻 &nbsp; Geek 时间
                        </div>
                    </header>

                    <article className="text-sky-50 p-4 overflow-y-auto"  style={{ whiteSpace: 'pre-line' }}>
                        <p className="text-sm font-bold">{event.content.title}</p>
                        
                        <hr className="my-2 border-t border-gray-300" />

                        <div className="flex items-center space-x-2">
                            <p className="text-xs text-gray-200/70">{event.content.name}</p>
                            <p className="text-xs text-gray-200/70">{event.content.time}</p>
                        </div>

                        <p className="text-xs py-2 text-sky-50">{event.content.content}</p>
                    </article>
                </div>
            )}

            {event.type === "search" && (
                <div className="fixed right-5 bottom-5 w-80 h-2/5 flex p-0 bg-opacity-30 shadow-lg backdrop-blur-sm duration-500" style={{ userSelect: 'none' }}>
                    <header className="bg-gray-600 bg-opacity-30 p-4 flex items-center justify-center text-base text-sky-50">
                        <div className="breathing-light align-middle" style={{writingMode: 'vertical-rl'}}>
                            🔍 &nbsp; 正在搜索
                        </div>
                    </header>
                    <article class="text-xs text-sky-50 p-4 overflow-y-auto"  style={{ whiteSpace: 'pre-line' }}>
                        <div className='flex justify-between items-center space-x-2 text-sm'>
                            <input type='text' className='px-2 rounded-lg bg-transparent border w-4/5 truncate' value={event.query} readOnly />
                            <button disabled>搜索</button>
                        </div>
                        
                        <hr className="my-2 border-t border-gray-300" />

                        {event.results.map((result, index) => (
                            <div key={index}>
                                <p className="text-xs font-bold">{result.title}</p>
                                <p className="text-xs text-gray-200/90">{result.body}</p>
                                <hr className="my-2 border-t border-gray-300" />
                            </div>
                        ))}
                    </article>
                </div>
            )}

            {event.type === "post_weibo" && (
                <div className="fixed right-5 bottom-5 w-80 h-2/5 flex p-0 bg-opacity-30 shadow-lg backdrop-blur-sm duration-500" style={{ userSelect: 'none' }}>
                    <header className="bg-gray-600 bg-opacity-30 p-4 flex items-center justify-center text-base text-sky-50">
                        <div className="breathing-light align-middle" style={{writingMode: 'vertical-rl'}}>
                            🧣 &nbsp; 发布微博
                        </div>
                    </header>
                    <article className="relative">
                        { event.weibo_url ? (
                            <>
                                <iframe
                                    src={event.weibo_url}
                                    width="100%"
                                    height="100%"
                                    allowtransparency="true"
                                    allow="encrypted-media"
                                />
                            </>
                        ) : (
                            <span className="text-sm text-sky-50 p-4 flex justify-center items-center">
                                糟糕，网络好像出了点问题，微博发布失败！
                            </span>
                        )}
                    </article>
                </div>
            )}

            {event.type === "check_weibo_comments" && (
                <div className="fixed right-5 bottom-5 w-80 h-2/5 flex p-0 bg-opacity-30 shadow-lg backdrop-blur-sm duration-500" style={{ userSelect: 'none' }}>
                    <header className="bg-gray-600 bg-opacity-30 p-4 flex items-center justify-center text-base text-sky-50">
                        <div className="breathing-light align-middle" style={{writingMode: 'vertical-rl'}}>
                            🧣 &nbsp; 正在翻微博评论
                        </div>
                    </header>
                    <article class="text-xs text-sky-50 p-4 overflow-y-auto"  style={{ whiteSpace: 'pre-line' }}>
                        { event.weibo_info ? (
                            <div className='px-2 text-sm'>
                                <span className="text-sky-50 font-bold">{event.weibo_info.content}</span>
                                <div className="flex space-x-2">
                                    <span className='text-gray-200/70 text-xs'>{event.weibo_info.created_at}</span>
                                    <span className='text-gray-200/70 text-xs'>{event.weibo_info.region_name}</span>
                                </div>
                            </div>
                            ) : (
                                <span className="text-sm text-sky-50 p-4 flex justify-center items-center">
                                    糟糕，网络好像出了点问题，微博评论获取失败！
                                </span>
                            )
                        }
                        
                        <hr className="my-2 border-t-4 border-gray-300" />

                        {event.comments.map((result, index) => (
                            <div key={index} className="my-1">
                                <p className="text-xs font-bold inline">@{result.user_name}：</p>
                                <p className="text-xs inline">{result.content}</p>

                                <div className="flex">
                                    <p className="text-xs text-gray-200/70 inline"> {result.created_at}</p>
                                    <div className="flex ml-auto space-x-1">
                                        <div className=" underline underline-offset-2">
                                            回复
                                        </div>
                                        <div className="underline underline-offset-2">
                                            点赞
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </article>
                </div>
            )}

            {event.type === "reply_weibo_comment" && (
                <div className="fixed right-5 bottom-5 w-80 h-2/5 flex p-0 bg-opacity-30 shadow-lg backdrop-blur-sm duration-500" style={{ userSelect: 'none' }}>
                    <header className="bg-gray-600 bg-opacity-30 p-4 flex items-center justify-center text-base text-sky-50">
                        <div className="breathing-light align-middle" style={{writingMode: 'vertical-rl'}}>
                            🧣 &nbsp; 回复微博评论
                        </div>
                    </header>
                    <article class="text-xs text-sky-50 p-2 overflow-y-auto"  style={{ whiteSpace: 'pre-line' }}>
                        { event.comment_content ? (
                            <>
                                <div className="my-2">
                                    <span className="text-sm font-bold">选择回复评论</span>
                                </div>

                                <div className="my-2">
                                    <p className="inline">@</p>
                                    <p className="text-xs font-bold inline underline underline-offset-2">{event.user_name}</p>
                                    <p className="inline">： </p>
                                    <p className="text-xs inline">{event.comment_content}</p>
                                </div>

                                <div className="mx-2">
                                    <p className="inline">|_@ </p>
                                    <p className="inline underline underline-offset-2">你 </p>
                                    <p className="inline"> 回复了：</p>
                                    <p className="inline">{event.reply_content}</p>
                                </div>

                                <div className="flex space-x-1 mr-4">
                                    <div className="ml-auto underline underline-offset-2">
                                        回复
                                    </div>
                                    <div className="ml-auto underline underline-offset-2">
                                        点赞
                                    </div>
                                </div>
                            </>
                            ) : (
                                <span className="text-sm text-sky-50 p-4 flex justify-center items-center">
                                    糟糕，网络好像出了点问题，微博评论回复失败！
                                </span>
                            )
                        }

                    </article>
                </div>
            )}

            {event.type === "find_leetcode_list" && (
                <div className="fixed right-5 bottom-5 w-80 h-2/5 flex p-0 bg-opacity-30 shadow-lg backdrop-blur-sm duration-500" style={{ userSelect: 'none' }}>
                    <header className="bg-gray-600 bg-opacity-30 p-4 flex items-center justify-center text-base text-sky-50">
                        <div className="breathing-light align-middle" style={{writingMode: 'vertical-rl'}}>
                        💻 &nbsp; LeetCode 时间
                        </div>
                    </header>

                    <article class="text-sm text-sky-50 overflow-y-auto overflow-x-hidden"  style={{ whiteSpace: 'pre-line' }}>
                        {event.questions.map((result, index) => (
                            <div key={index}>
                                <div className="flex justify-between items-center px-2">
                                    <p className="truncate">{index + 1}. {result.title}</p>
                                    <p className={`rounded px-2 ${result.difficulty === 'EASY' ? 'text-green-200 bg-green-400' : result.difficulty === 'HARD' ? 'text-red-200 bg-red-400' : 'text-yellow-200 bg-yellow-400'}`}>
                                        {result.difficulty}
                                    </p>
                                </div>
                                <hr className="my-2 border-t border-gray-300" />
                            </div>
                        ))}
                    </article>
                </div>
            )}

            {event.type === "complete_leetcode_question" && (
                <div className="fixed right-5 bottom-5 w-1/3 h-2/5 flex flex-col p-0 bg-opacity-30 shadow-lg backdrop-blur-sm duration-500 rounded-md" style={{ userSelect: 'none' }}>
                    <header className="bg-gray-600 bg-opacity-30 p-4 h-10 flex items-center justify-center text-base text-sky-50 rounded-md">
                        <div className="breathing-light align-middle">
                        💻 &nbsp; LeetCode 时间
                        </div>
                    </header>

                    {/* {JSON.stringify(event.code_result)} */}

                    <div class="text-sm text-sky-50 overflow-y-auto flex"  style={{ whiteSpace: 'pre-line' }}>
                        <div className="w-1/2 overflow-y-auto border-r p-2">
                            <article className="font-bold text-base">{event.question_details.translatedTitle}</article>
                            <br />
                            <article dangerouslySetInnerHTML={{ __html: event.question_details.translatedContent }} />
                        </div>
                        <div className="flex flex-col overflow-y-auto p-2">
                            <pre className="border-b h-2/3 overflow-y-auto">
                            <SyntaxHighlighter language="python" style={nightOwl} customStyle={{ background: "transparent" }}>
                                    {event.code}
                                </SyntaxHighlighter>
                            </pre>
                            
                            <div className="p-2 space-y-1 h-1/3 overflow-y-auto">
                                <p>输入：{event.question_details.test_case}</p>
                                <p>期望运行结果：{event.code_result.expected_code_answer}</p>
                                <p>实际运行结果：{event.code_result.code_answer}</p>
                                <p>正确与否：<span className={`${event.code_result.correct_answer ? 'text-green-200' : 'text-red-200'}`}>
                                    {event.code_result.correct_answer ? 'TRUE' : 'FALSE'}
                                </span></p>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </>
    )
}

export default EventBox