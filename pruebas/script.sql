USE [master]
GO
/****** Object:  Database [micau5a]    Script Date: 1/5/2024 17:21:23 ******/
CREATE DATABASE [micau5a]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'micau5a', FILENAME = N'G:\FerozoDatabases\sqlsrv\data\micau5a.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'micau5a_log', FILENAME = N'G:\FerozoDatabases\sqlsrv\log\micau5a_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [micau5a] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [micau5a].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [micau5a] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [micau5a] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [micau5a] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [micau5a] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [micau5a] SET ARITHABORT OFF 
GO
ALTER DATABASE [micau5a] SET AUTO_CLOSE ON 
GO
ALTER DATABASE [micau5a] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [micau5a] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [micau5a] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [micau5a] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [micau5a] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [micau5a] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [micau5a] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [micau5a] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [micau5a] SET  ENABLE_BROKER 
GO
ALTER DATABASE [micau5a] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [micau5a] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [micau5a] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [micau5a] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [micau5a] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [micau5a] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [micau5a] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [micau5a] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [micau5a] SET  MULTI_USER 
GO
ALTER DATABASE [micau5a] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [micau5a] SET DB_CHAINING OFF 
GO
ALTER DATABASE [micau5a] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [micau5a] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [micau5a] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [micau5a] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
ALTER DATABASE [micau5a] SET QUERY_STORE = OFF
GO
USE [micau5a]
GO
/****** Object:  User [daniel]    Script Date: 1/5/2024 17:21:23 ******/
CREATE USER [daniel] FOR LOGIN [daniel] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [basti]    Script Date: 1/5/2024 17:21:23 ******/
CREATE USER [basti] FOR LOGIN [basti] WITH DEFAULT_SCHEMA=[db_datareader]
GO
ALTER ROLE [db_owner] ADD MEMBER [daniel]
GO
ALTER ROLE [db_accessadmin] ADD MEMBER [daniel]
GO
ALTER ROLE [db_securityadmin] ADD MEMBER [daniel]
GO
ALTER ROLE [db_ddladmin] ADD MEMBER [daniel]
GO
ALTER ROLE [db_backupoperator] ADD MEMBER [daniel]
GO
ALTER ROLE [db_datareader] ADD MEMBER [daniel]
GO
ALTER ROLE [db_datawriter] ADD MEMBER [daniel]
GO
ALTER ROLE [db_denydatareader] ADD MEMBER [daniel]
GO
ALTER ROLE [db_denydatawriter] ADD MEMBER [daniel]
GO
ALTER ROLE [db_accessadmin] ADD MEMBER [basti]
GO
ALTER ROLE [db_datareader] ADD MEMBER [basti]
GO
ALTER ROLE [db_datawriter] ADD MEMBER [basti]
GO
/****** Object:  Table [dbo].[actuaciones]    Script Date: 1/5/2024 17:21:23 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[actuaciones](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[numjui] [varchar](255) NULL,
	[nombTribunal] [varchar](255) NULL,
	[tipojuicio] [varchar](255) NULL,
	[actuacion] [varchar](255) NULL,
	[fecha] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[numjui] ASC,
	[nombTribunal] ASC,
	[tipojuicio] ASC,
	[actuacion] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[AUD_notificacion]    Script Date: 1/5/2024 17:21:23 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[AUD_notificacion](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[fechaNotificacion] [datetime] NULL,
	[numjui] [varchar](255) NULL,
	[nombTribunal] [varchar](255) NULL,
	[demandante] [varchar](255) NULL,
	[demandado] [varchar](255) NULL,
	[repre] [varchar](255) NULL,
	[mandante] [varchar](255) NULL,
	[domicilio] [varchar](255) NULL,
	[comuna] [varchar](255) NULL,
	[encargo] [varchar](255) NULL,
	[soli] [varchar](255) NULL,
	[arancel] [int] NULL,
	[estadoNoti] [int] NULL,
	[estadoCausa] [int] NULL,
	[actu] [varchar](255) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[buscar_historico]    Script Date: 1/5/2024 17:21:23 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[buscar_historico](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[fechaNotificacion] [datetime] NULL,
	[numjui] [varchar](255) NULL,
	[nombTribunal] [varchar](255) NULL,
	[demandante] [varchar](255) NULL,
	[demandado] [varchar](255) NULL,
	[repre] [varchar](255) NULL,
	[mandante] [varchar](255) NULL,
	[domicilio] [varchar](255) NULL,
	[comuna] [varchar](255) NULL,
	[encargo] [varchar](255) NULL,
	[soli] [varchar](255) NULL,
	[arancel] [int] NULL,
	[estadoNoti] [int] NULL,
	[estadoCausa] [int] NULL,
	[actu] [varchar](255) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[demanda]    Script Date: 1/5/2024 17:21:23 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[demanda](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[numjui] [varchar](255) NULL,
	[nombTribunal] [varchar](255) NULL,
	[demandante] [varchar](255) NULL,
	[demandado] [varchar](255) NULL,
	[repre] [varchar](255) NULL,
	[mandante] [varchar](255) NULL,
	[domicilio] [varchar](255) NULL,
	[comuna] [varchar](255) NULL,
	[encargo] [varchar](255) NULL,
	[soli] [varchar](255) NULL,
	[arancel] [int] NULL,
	[actu] [varchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[numjui] ASC,
	[nombTribunal] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[historico]    Script Date: 1/5/2024 17:21:23 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[historico](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[numJui] [varchar](255) NULL,
	[tribunal] [varchar](255) NULL,
	[tipoEstampado] [varchar](255) NULL,
	[mandante] [varchar](255) NULL,
	[arancel] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[notificacion]    Script Date: 1/5/2024 17:21:23 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[notificacion](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[fechaNotificacion] [datetime] NULL,
	[numjui] [varchar](255) NULL,
	[nombTribunal] [varchar](255) NULL,
	[demandante] [varchar](255) NULL,
	[demandado] [varchar](255) NULL,
	[repre] [varchar](255) NULL,
	[mandante] [varchar](255) NULL,
	[domicilio] [varchar](255) NULL,
	[comuna] [varchar](255) NULL,
	[encargo] [varchar](255) NULL,
	[soli] [varchar](255) NULL,
	[arancel] [int] NULL,
	[estadoNoti] [int] NULL,
	[estadoCausa] [int] NULL,
	[actu] [varchar](255) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[usuarios]    Script Date: 1/5/2024 17:21:23 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[usuarios](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[username] [varchar](225) NOT NULL,
	[nombreusuario] [varchar](255) NOT NULL,
	[apellidousuario] [varchar](255) NOT NULL,
	[password] [varchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  StoredProcedure [dbo].[EliminarNotificaciones]    Script Date: 1/5/2024 17:21:23 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[EliminarNotificaciones]
AS
DELETE FROM notificacion
WHERE estadoNoti = 1 AND UltimaActualizacionEstadoNoti < DATEADD(MINUTE, -12, GETDATE());
GO
USE [master]
GO
ALTER DATABASE [micau5a] SET  READ_WRITE 
GO
