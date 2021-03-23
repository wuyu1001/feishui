module.exports = {
    publicPath: "./", // 公共路径(必须有的)
    outputDir: "dist", // 输出文件目录
    assetsDir: "static", //静态资源文件名称
    lintOnSave: false,
    productionSourceMap: false, //去除打包后js的map文件
    devServer: { //启动项目在8080端口自动打开
        open: true,
        port: 8080,
        proxy: null
    },
    //去掉console
    configureWebpack: (config) => {
        // 判断为生产模式下，因为开发模式我们是想保存console的
        if (process.env.NODE_ENV === "production") {
            config["performance"] = {//打包文件大小配置
                "maxEntrypointSize": 10000000,
                "maxAssetSize": 30000000
            },
                config.optimization.minimizer.map((arg) => {
                    const option = arg.options.terserOptions.compress;
                    option.drop_console = true; // 打开开关
                    return arg;
                });
        }
    },
};